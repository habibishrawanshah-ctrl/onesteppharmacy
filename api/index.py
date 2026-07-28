import os
import sys

project = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pharmacy_ecommerce')
sys.path.insert(0, project)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_ecommerce.settings')

if os.environ.get('VERCEL'):
    import django
    django.setup()
    from django.db import connection
    tables = connection.introspection.table_names()
    if 'products_product' not in tables:
        from django.core.management import call_command
        call_command('migrate')
        from products.models import Product
        if Product.objects.count() == 0:
            exec(open(os.path.join(project, 'scripts', 'seed_prod.py')).read().split('if __name__')[0] + 'seed()')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
