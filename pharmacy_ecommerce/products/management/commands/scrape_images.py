import re
import requests
import concurrent.futures
import xml.etree.ElementTree as ET
from collections import defaultdict
from difflib import SequenceMatcher
from django.core.management.base import BaseCommand
from products.models import Product


SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
})

STOPWORDS = {
    'tablets', 'tablet', 'capsules', 'capsule', 'pack', 'bottle', 'roll',
    'pieces', 's', 'plus', 'forte', 'sr', 'xl', 'ds', 'mr', 'sp',
    'mg', 'ml', 'g', 'gm', 'mcg', 'iu', 'syrup', 'spray', 'gel',
    'cream', 'ointment', 'drop', 'drops', 'injection', 'powder',
    'of', 'for', 'and', 'with', 'the', 'in',
}

GENERIC = {
    'tablet.jpg', 'capsule.jpg', 'syrup.jpg', 'gel.jpg', 'powder.jpg',
    'injection.jpg', 'expectorant.jpg', 'cream.jpg', 'lotion.jpg',
    'spray.jpg', 'oral_drops.jpg', 'eye_drops.jpg', 'oil.jpg',
    'sachet.jpg', 'oral_gel.jpg', 'softgels.jpg',
}

UNSPLASH_POOL = [
    'https://images.unsplash.com/photo-1587854692152-cbe660dbde88',
    'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b',
    'https://images.unsplash.com/photo-1550572017-edd951b55104',
    'https://images.unsplash.com/photo-1631549916768-4119b2e5f926',
    'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae',
    'https://images.unsplash.com/photo-1471864190281-a93a3070b6de',
    'https://images.unsplash.com/photo-1585435557343-3b092031a831',
    'https://images.unsplash.com/photo-1577174881658-0f30ed549adc',
    'https://images.unsplash.com/photo-1544947950-fa07a98d237f',
    'https://images.unsplash.com/photo-1550572017-edd951b55104',
]


def resolve_sitemap(url):
    r = SESSION.get(url, timeout=15)
    root = ET.fromstring(r.content)
    if 'sitemapindex' in root.tag:
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        results = []
        for loc in root.findall('.//sm:loc', ns):
            results.extend(resolve_sitemap(loc.text))
        return results
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    return [loc.text for loc in root.findall('.//sm:loc', ns)]


def extract_og_image(url):
    try:
        r = SESSION.get(url, timeout=15)
        if r.status_code != 200:
            return None
        for pat in [
            r'<meta\s+property="og:image"\s+content="([^"]+)"',
            r'<meta\s+name="twitter:image"\s+content="([^"]+)"',
        ]:
            m = re.search(pat, r.text)
            if m:
                url = m.group(1).split('?')[0]
                name = url.rsplit('/', 1)[-1]
                if 'catalog/product/' in url and name not in GENERIC:
                    return url
                return None
    except Exception:
        pass
    return None


class Command(BaseCommand):
    help = 'Scrape real product images from Apollo Pharmacy'

    def add_arguments(self, parser):
        parser.add_argument('--workers', type=int, default=5)

    def handle(self, *args, **options):
        workers = options['workers']

        self.stdout.write('Downloading OTC sitemaps...')
        resp = SESSION.get('https://www.apollopharmacy.in/sitemap/sitemap-master.xml', timeout=15)
        root = ET.fromstring(resp.content)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        otc_maps = [loc.text for loc in root.findall('.//sm:loc', ns) if 'pharma-otc' in loc.text]

        all_urls = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            for urls in ex.map(resolve_sitemap, otc_maps):
                all_urls.extend(urls)

        by_prefix = defaultdict(list)
        for url in all_urls:
            slug = url.rstrip('/').rsplit('/', 1)[-1]
            by_prefix[slug.split('-')[0]].append((slug, url))
        self.stdout.write(f'{len(by_prefix)} prefix entries from {len(all_urls)} URLs')

        products = list(Product.objects.filter(image__isnull=True) | Product.objects.filter(image=''))
        self.stdout.write(f'{len(products)} products need images')

        matches = []
        for p in products:
            parts = re.sub(r"[,'()]+", '', p.name.lower()).split()
            brand = []
            for part in parts:
                c = re.sub(r'[^a-z0-9]', '', part)
                if c and c not in STOPWORDS:
                    brand.append(c)
                else:
                    break
            if not brand:
                continue
            best_score, best_url = 0, None
            seen = set()
            for b in brand:
                for slug, url in by_prefix.get(b, []):
                    if url in seen:
                        continue
                    seen.add(url)
                    n = re.sub(r'[^a-z0-9\s]', '', p.name.lower()).strip()
                    s = slug.replace('-', ' ').strip()
                    score = SequenceMatcher(None, n, s).ratio()
                    if score > best_score:
                        best_score, best_url = score, url
            if best_score > 0.35 and best_url:
                matches.append((p, best_url))

        self.stdout.write(f'Matched {len(matches)} to Apollo URLs')

        if matches:
            def fetch(item):
                p, url = item
                img = extract_og_image(url)
                if img:
                    p.image = img
                    p.save(update_fields=['image'])
                    return (p.name, img, True)
                if 'otc/' in url:
                    img = extract_og_image(url.replace('otc/', 'medicine/'))
                    if img:
                        p.image = img
                        p.save(update_fields=['image'])
                        return (p.name, img, True)
                return (p.name, None, False)

            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
                results = list(ex.map(fetch, matches))

            success = sum(1 for r in results if r[2])
            self.stdout.write(f'Found {success} real product images')

        still_missing = list(Product.objects.filter(image__isnull=True) | Product.objects.filter(image=''))
        self.stdout.write(f'Unsplash fallback for {len(still_missing)} products')
        for p in still_missing:
            p.image = UNSPLASH_POOL[abs(hash(p.name)) % len(UNSPLASH_POOL)] + '?w=400&q=80'
            p.save(update_fields=['image'])

        total = Product.objects.exclude(image__isnull=True).exclude(image__exact='').count()
        self.stdout.write(self.style.SUCCESS(f'{total}/{Product.objects.count()} have images'))
