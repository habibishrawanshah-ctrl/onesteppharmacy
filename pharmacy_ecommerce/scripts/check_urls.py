import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_ecommerce.settings')
import django
django.setup()
from django.test import Client
c = Client()
for path in ['/login/', '/orders/place/1/', '/orders/success/', '/products/']:
    r = c.get(path, HTTP_HOST='127.0.0.1')
    print(path, r.status_code, getattr(r, 'url', ''), len(r.content))
