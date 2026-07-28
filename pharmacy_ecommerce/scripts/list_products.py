import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pharmacy_ecommerce.settings')
django.setup()
from products.models import Product
for p in Product.objects.all():
    print(p.id, p.name, p.image.name if p.image else None, p.stock, p.price)
