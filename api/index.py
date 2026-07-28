import os
import sys
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pharmacy_ecommerce'))

if os.environ.get('VERCEL'):
    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pharmacy_ecommerce', 'db.sqlite3')
    dst = '/tmp/db.sqlite3'
    if not os.path.exists(dst) and os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        os.chmod(dst, 0o666)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_ecommerce.settings')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
