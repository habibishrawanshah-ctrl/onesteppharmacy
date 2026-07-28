import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pharmacy_ecommerce'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_ecommerce.settings')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
