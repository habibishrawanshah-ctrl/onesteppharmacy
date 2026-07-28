import os, sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pharmacy_ecommerce.settings')
import django
django.setup()
from django.test import Client
c=Client()
for path in ['/','/products/','/products/1/']:
    r=c.get(path)
    print(path, r.status_code, [t.name for t in getattr(r,'templates',[])])
