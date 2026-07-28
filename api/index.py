import os
import sys
import shutil

project = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pharmacy_ecommerce')
sys.path.insert(0, project)

if os.environ.get('VERCEL'):
    src = os.path.join(project, 'db.sqlite3')
    dst = '/tmp/db.sqlite3'
    if os.path.exists(src) and not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_ecommerce.settings')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
