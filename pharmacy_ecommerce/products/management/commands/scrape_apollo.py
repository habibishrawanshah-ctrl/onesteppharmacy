import requests
import re
import time
from django.core.management.base import BaseCommand
from products.models import Product, Category


CATEGORY_NAMES = {
    'health-devices': 'Health Devices',
    'pain-relief': 'Pain Relief',
    'cold-cough': 'Cold & Cough',
    'stomach-care': 'Stomach Care',
    'vitamins-minerals': 'Vitamins & Minerals',
    'diabetic-care': 'Diabetic Care',
    'blood-pressure': 'Blood Pressure',
    'skin-care-1': 'Skin Care',
    'wound-care-1': 'Wound Care',
    'nutritional-drinks-supplements': 'Nutritional Drinks & Supplements',
    'cardiac-care': 'Cardiac Care',
    'eye-care-1': 'Eye Care',
    'bone-joint-muscle': 'Bone, Joint & Muscle',
    'respiratory': 'Respiratory Care',
    'liver-care': 'Liver Care',
    'sexual-wellness-1': 'Sexual Wellness',
    'baby-care': 'Baby Care',
    'oral-care-1': 'Oral Care',
}


class Command(BaseCommand):
    help = 'Scrape products from Apollo Pharmacy categories'

    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, default=3, help='Number of pages to scrape')
        parser.add_argument('--category', type=str, default='health-devices',
            help=f'Category slug. One of: {", ".join(CATEGORY_NAMES.keys())}')

    def handle(self, *args, **options):
        pages = options['pages']
        category_slug = options['category']
        cat_name = CATEGORY_NAMES.get(category_slug, category_slug.replace('-', ' ').title())
        cat, _ = Category.objects.get_or_create(name=cat_name, slug=category_slug)
        total = 0

        for page in range(1, pages + 1):
            self.stdout.write(f'Scraping page {page}...')
            url = f'https://www.apollopharmacy.in/shop-by-category/{category_slug}?page={page}'
            try:
                resp = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml',
                }, timeout=15)
                html = resp.text
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to fetch page {page}: {e}'))
                continue

            products = self._extract_products(html)
            for pdata in products:
                Product.objects.get_or_create(
                    name=pdata['name'][:100],
                    defaults={
                        'category': cat,
                        'description': pdata.get('description', ''),
                        'price': pdata['price'],
                        'stock': pdata.get('stock', 50),
                        'manufacturer': pdata.get('manufacturer', 'Apollo Pharmacy'),
                    }
                )
                total += 1

            time.sleep(2)

        self.stdout.write(self.style.SUCCESS(f'Imported {total} products into {cat_name}'))

    def _extract_products(self, html):
        products = []
        seen = set()

        price_pattern = re.compile(r'₹([\d,]+\.?\d*)')
        name_pattern = re.compile(r'\"name\":\"([^\"]+)\"')

        for match in re.finditer(r'\"name\":\"([^\"]+)\".*?\"price\":([\d.]+)', html, re.DOTALL):
            name = match.group(1)
            price_str = match.group(2)
            if name in seen or len(name) < 5:
                continue
            seen.add(name)
            try:
                price_val = float(price_str)
            except ValueError:
                continue
            if price_val > 0:
                products.append({
                    'name': name,
                    'price': price_val,
                    'stock': 50,
                    'manufacturer': 'Apollo Pharmacy',
                })

        if not products:
            for match in re.finditer(r'>([^<]{10,300})<', html):
                text = match.group(1).strip()
                prices = price_pattern.findall(text)
                if not prices:
                    continue
                pname_match = re.search(r'([A-Z][A-Za-z0-9\s\-&,()/]+?)(?:\s*₹|\s*MRP)', text)
                if not pname_match:
                    continue
                name = pname_match.group(1).strip()
                if len(name) < 10 or name in seen:
                    continue
                if any(x in name.lower() for x in ['sort by', 'filter', 'brand', 'page', 'items', 'show']):
                    continue
                seen.add(name)
                try:
                    price_val = float(prices[0].replace(',', ''))
                except ValueError:
                    continue
                if price_val > 0:
                    products.append({
                        'name': name,
                        'price': price_val,
                        'stock': 50,
                        'manufacturer': 'Apollo Pharmacy',
                    })

        return products[:50]
