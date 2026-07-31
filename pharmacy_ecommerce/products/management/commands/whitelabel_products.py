from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'White-label all products: replace Apollo branding with OneStep Pharmacy'

    def handle(self, *args, **options):
        renamed = 0
        remanufactured = 0
        redescribed = 0
        for product in Product.objects.all():
            changed = False

            old_name = product.name
            product.name = product.name.replace('Apollo Pharmacy', 'OneStep')
            product.name = product.name.replace('Apollo Life', 'OneStep')
            if product.name != old_name:
                renamed += 1
                changed = True
                self.stdout.write(f'  Renamed: {old_name[:60]} -> {product.name[:60]}')

            if 'Apollo' in product.description:
                product.description = product.description.replace('Apollo Pharmacy', 'OneStep')
                product.description = product.description.replace('Apollo Life', 'OneStep')
                redescribed += 1
                changed = True

            if product.manufacturer == 'Apollo Pharmacy':
                product.manufacturer = 'OneStep Pharmacy'
                remanufactured += 1
                changed = True

            if changed:
                product.save()

        self.stdout.write(self.style.SUCCESS(
            f'Done: {renamed} renamed, {redescribed} redescribed, {remanufactured} remanufactured'
        ))
