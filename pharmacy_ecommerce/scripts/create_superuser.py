import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_ecommerce.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()

USERNAME = 'habibi@123'
PASSWORD = '6X 10X'
EMAIL = ''

u = None
if User.objects.filter(username=USERNAME).exists():
    u = User.objects.get(username=USERNAME)
    u.set_password(PASSWORD)
    u.email = EMAIL
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('updated superuser', USERNAME)
else:
    u = User.objects.create_user(username=USERNAME, email=EMAIL)
    u.set_password(PASSWORD)
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('created superuser', USERNAME)
