import requests
import re
import time
from django.core.management.base import BaseCommand
from products.models import Product, Category
from io import StringIO


class Command(BaseCommand):
    help = 'Scrape products from Apollo Pharmacy health-devices category'

    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, default=3, help='Number of pages to scrape')
        parser.add_argument('--category', type=str, default='health-devices', help='Category slug')

    def handle(self, *args, **options):
        pages = options['pages']
        category_slug = options['category']
        cat, _ = Category.objects.get_or_create(name='Health Devices', slug='health-devices')
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

            # Try to extract product data from Next.js RSC payload
            products = self._extract_products(html, cat)
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

        self.stdout.write(self.style.SUCCESS(f'Imported {total} products'))

    def _extract_products(self, html, cat):
        products = []
        seen = set()

        # Pattern 1: Look for product data in RSC payload (JSON-like strings)
        # Find strings containing product name and price
        price_pattern = re.compile(r'₹([\d,]+\.?\d*)')
        name_pattern = re.compile(r'([A-Z][A-Za-z0-9\s\-&,()]+)(?:\s*₹|\s*MRP)')

        # Extract text segments with prices
        for match in re.finditer(r'>([^<]{10,300})<', html):
            text = match.group(1).strip()
            prices = price_pattern.findall(text)
            names = name_pattern.findall(text)

            for name in names:
                name = name.strip()
                if len(name) < 10 or name in seen:
                    continue
                # Skip non-product text
                if any(x in name.lower() for x in ['sort by', 'filter', 'brand', 'page', 'items']):
                    continue
                seen.add(name)

                # Find nearest price
                price_val = 0
                for p in prices:
                    try:
                        price_val = float(p.replace(',', ''))
                        break
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
