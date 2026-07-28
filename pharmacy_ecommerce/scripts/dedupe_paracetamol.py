import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_ecommerce.settings')
import django
django.setup()
from products.models import Product

# match variants of paracetamol / paractamol
qs = Product.objects.filter(name__icontains='parac')
print('found', qs.count(), 'matching products')
if qs.count() <= 1:
    print('nothing to do')
else:
    keep = qs.order_by('id').first()
    to_delete = qs.exclude(id=keep.id)
    print('keeping id', keep.id, 'name', keep.name)
    del_ids = [p.id for p in to_delete]
    print('deleting ids', del_ids)
    to_delete.delete()
    print('deleted')
