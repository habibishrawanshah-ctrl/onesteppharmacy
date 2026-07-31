import os
import re
import io
import json
from urllib.parse import urljoin

import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from products.models import Product, Category

import cloudinary
import cloudinary.uploader


def clean_name(name):
    name = re.sub(r'&amp;', '&', name)
    name = re.sub(r'&\w+;', '', name)
    return name.strip()


class Command(BaseCommand):
    help = 'Scrape products + real images from Apollo Pharmacy category pages, store locally and push to Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument('--category-slug', default='health-devices', help='Category slug to scrape (default: health-devices)')
        parser.add_argument('--max-pages', type=int, default=3, help='Max pages to scrape')
        parser.add_argument('--local-dir', default='product_images', help='Local media subdirectory')
        parser.add_argument('--dry-run', action='store_true', help='Only print matched products, do not save')

    def scrape_category(self, category_slug, max_pages):
        products = []
        for page in range(1, max_pages + 1):
            url = f'https://www.apollopharmacy.in/shop-by-category/{category_slug}'
            if page > 1:
                url += f'?page={page}'
            self.stdout.write(f'Fetching {url} ...')
            resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
            if resp.status_code != 200:
                self.stdout.write(self.style.WARNING(f'  HTTP {resp.status_code}, stopping'))
                break
            html = resp.text
            cards = re.findall(
                r'<a href="/(?:otc|medicine)/[^"]+" class="cardAnchorStyle[^"]*" aria-label="([^"]+)".*?'
                r'<img srcSet="(https://images\.apollo247\.in/pub/media/catalog/product/[^?"\s]+)[^"]*".*?'
                r'₹\s*<!--\s*-->?\s*([\d.]+)</p>',
                html, re.S)
            if not cards:
                self.stdout.write(self.style.WARNING(f'  No product cards found, stopping'))
                break
            for alt, img_url, price in cards:
                products.append({'name': clean_name(alt), 'image_url': img_url, 'price': price})
            self.stdout.write(f'  {len(cards)} products on page {page}')
        return products

    def download_image(self, url):
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        if resp.status_code != 200:
            return None
        ext = '.jpg'
        m = re.search(r'\.(jpe?g|png|webp)(?:[?#]|$)', url, re.I)
        if m:
            ext = '.' + m.group(1).lower()
        return resp.content, ext

    def handle(self, *args, **options):
        category_slug = options['category_slug']
        max_pages = options['max_pages']
        local_dir = options['local_dir']
        dry_run = options['dry_run']

        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', 'cxfqn4a3'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        )

        scraped = self.scrape_category(category_slug, max_pages)
        seen = set()
        unique = []
        for item in scraped:
            if item['name'] in seen:
                continue
            seen.add(item['name'])
            unique.append(item)
        scraped = unique
        self.stdout.write(self.style.SUCCESS(f'Scraped {len(scraped)} unique products from Apollo'))

        cat, created = Category.objects.get_or_create(name='Health Devices', slug=category_slug)
        if created:
            self.stdout.write(f'Created category: {cat.name}')

        local_dir_path = os.path.join(settings.MEDIA_ROOT, local_dir)
        os.makedirs(local_dir_path, exist_ok=True)

        uploaded = 0
        saved = 0
        failed = 0
        for item in scraped:
            name = item['name'][:100]
            if len(item['name']) > 100:
                name = name.rsplit(' ', 1)[0]
            try:
                product = Product.objects.get(name__iexact=name)
            except Product.DoesNotExist:
                product = None

            if product is None:
                if dry_run:
                    self.stdout.write(f'  NEW (not in DB): {name}')
                    continue
                product = Product.objects.create(
                    category=cat,
                    name=name,
                    description=item['name'],
                    price=item['price'] or 0,
                    stock=10,
                    manufacturer='Apollo Pharmacy',
                )
                self.stdout.write(f'  Created: {name}')
            elif product.image and product.image.name and 'cloudinary.com' in product.image.name:
                self.stdout.write(f'  SKIP (already has Cloudinary image): {name}')
                continue

            img = self.download_image(item['image_url'])
            if img is None:
                self.stdout.write(self.style.WARNING(f'  Image download failed: {name}'))
                failed += 1
                continue

            content, ext = img
            public_id = re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')
            if dry_run:
                self.stdout.write(f'  WOULD UPLOAD {public_id}{ext} for: {name}')
                continue

            local_filename = f'{public_id}{ext}'
            local_path = os.path.join(local_dir_path, local_filename)
            with open(local_path, 'wb') as f:
                f.write(content)
            self.stdout.write(f'  Saved locally: {local_path} ({len(content)} bytes)')

            result = cloudinary.uploader.upload(
                local_path,
                public_id=public_id,
                overwrite=True,
                folder='products',
                resource_type='image',
            )
            cloud_url = result.get('secure_url') or result.get('url')
            if not cloud_url:
                self.stdout.write(self.style.WARNING(f'  Cloudinary upload failed: {name}'))
                failed += 1
                continue
            product.image.name = cloud_url
            product.save(update_fields=['image'])
            uploaded += 1
            saved += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done: {saved} products saved, {uploaded} images uploaded to Cloudinary, {failed} failed '
            f'(total {len(scraped)} scraped)'
        ))
