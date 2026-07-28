import os
import sys
from pathlib import Path
# ensure project root is on path
sys.path.append(str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_ecommerce.settings')
import django
django.setup()
from products.models import Product
from django.utils import timezone

p, created = Product.objects.get_or_create(
    name='Paracetamol 500mg',
    defaults={
        'description': 'Effective pain relief and fever reducer. 20 tablets.',
        'price': 4.99,
        'stock': 120,
        'expiry_date': '2027-12-31',
        'image': 'product_images/paracetamol.svg',
    }
)
print('created=', created, 'id=', p.id)
