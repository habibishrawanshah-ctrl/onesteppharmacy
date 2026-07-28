import os
import sys
import django
from datetime import date, timedelta, datetime
from django.utils import timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_ecommerce.settings')
django.setup()

from django.core.files.base import ContentFile
from django.contrib.auth.models import User
import urllib.request
from products.models import Product
from orders.models import Order
from users.models import UserProfile

PRODUCT_DATA = [
    {
        'name': 'Paracetamol 500mg',
        'description': 'Effective pain reliever and fever reducer. Used for headaches, muscle aches, arthritis, backache, toothaches, colds, and fevers. Each tablet contains 500mg of paracetamol.',
        'price': 4.99, 'stock': 150, 'expiry_days': 730,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/a/a5/Medication_Paracetamol.JPG',
    },
    {
        'name': 'Ibuprofen 200mg',
        'description': 'Nonsteroidal anti-inflammatory drug (NSAID) used for relief of fever, mild to moderate pain, and inflammation.',
        'price': 6.99, 'stock': 200, 'expiry_days': 730,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/b/b0/200mg_ibuprofen_tablets.jpg',
    },
    {
        'name': 'Amoxicillin 500mg',
        'description': 'Broad-spectrum penicillin antibiotic used to treat bacterial infections including respiratory tract infections, ear infections, and skin infections.',
        'price': 12.99, 'stock': 80, 'expiry_days': 365,
        'image_url': 'https://images.pexels.com/photos/3683073/pexels-photo-3683073.jpeg',
    },
    {
        'name': 'Vitamin C 1000mg',
        'description': 'High-strength vitamin C supplement to support immune system function, collagen production, and antioxidant protection.',
        'price': 9.99, 'stock': 120, 'expiry_days': 1095,
        'image_url': 'https://images.pexels.com/photos/4047077/pexels-photo-4047077.jpeg',
    },
    {
        'name': 'Omeprazole 20mg',
        'description': 'Proton pump inhibitor (PPI) used to treat gastroesophageal reflux disease (GERD), stomach ulcers, and other conditions caused by excess stomach acid.',
        'price': 14.99, 'stock': 90, 'expiry_days': 730,
        'image_url': 'https://images.pexels.com/photos/3873149/pexels-photo-3873149.jpeg',
    },
    {
        'name': 'Cetirizine 10mg',
        'description': 'Antihistamine medication used to relieve allergy symptoms such as watery eyes, runny nose, itching eyes/nose, sneezing, and hives. 24-hour non-drowsy relief.',
        'price': 8.99, 'stock': 100, 'expiry_days': 730,
        'image_url': 'https://images.pexels.com/photos/9742778/pexels-photo-9742778.jpeg',
    },
    {
        'name': 'Aspirin 81mg',
        'description': 'Low-dose aspirin for cardiovascular protection. Enteric-coated for gentle on the stomach.',
        'price': 5.49, 'stock': 180, 'expiry_days': 1095,
        'image_url': 'https://images.pexels.com/photos/51929/medications-cure-tablets-pharmacy-51929.jpeg',
    },
    {
        'name': 'Multivitamin Complete',
        'description': 'Complete daily multivitamin and mineral supplement with vitamins A, C, D, E, B-complex, zinc, iron, and calcium.',
        'price': 15.99, 'stock': 60, 'expiry_days': 1095,
        'image_url': 'https://images.pexels.com/photos/5452239/pexels-photo-5452239.jpeg',
    },
    {
        'name': 'Metformin 500mg',
        'description': 'First-line medication for type 2 diabetes. Helps control blood sugar levels by improving insulin sensitivity.',
        'price': 7.99, 'stock': 110, 'expiry_days': 730,
        'image_url': 'https://images.pexels.com/photos/7526049/pexels-photo-7526049.jpeg',
    },
    {
        'name': 'Loratadine 10mg',
        'description': 'Non-drowsy antihistamine for seasonal allergy relief. 24-hour relief from sneezing, runny nose, itchy eyes.',
        'price': 7.49, 'stock': 130, 'expiry_days': 730,
        'image_url': 'https://images.pexels.com/photos/9742893/pexels-photo-9742893.jpeg',
    },
]

USERS = [
    {'username': 'admin', 'password': 'admin123', 'is_staff': True, 'is_superuser': True, 'address': '1 Admin Lane, HQ', 'phone': '+1-555-0100'},
    {'username': 'staff_jane', 'password': 'staffpass12', 'is_staff': True, 'is_superuser': False, 'address': '2 Staff Road', 'phone': '+1-555-0101'},
    {'username': 'alice', 'password': 'customer1A!', 'is_staff': False, 'is_superuser': False, 'address': '10 Customer Street', 'phone': '+1-555-0200'},
    {'username': 'bob', 'password': 'customer2B@', 'is_staff': False, 'is_superuser': False, 'address': '20 High Street', 'phone': '+1-555-0201'},
    {'username': 'carol', 'password': 'customer3C#', 'is_staff': False, 'is_superuser': False, 'address': '30 Market Road', 'phone': '+1-555-0202'},
    {'username': 'dave', 'password': 'customer4D$', 'is_staff': False, 'is_superuser': False, 'address': '40 Park Avenue', 'phone': '+1-555-0203'},
]

ORDERS = [
    {'username': 'alice', 'product': 'Paracetamol 500mg', 'qty': 2, 'status': 'Delivered', 'days_ago': 14},
    {'username': 'alice', 'product': 'Vitamin C 1000mg', 'qty': 1, 'status': 'Shipped', 'days_ago': 3},
    {'username': 'bob', 'product': 'Ibuprofen 200mg', 'qty': 1, 'status': 'Delivered', 'days_ago': 30},
    {'username': 'bob', 'product': 'Aspirin 81mg', 'qty': 3, 'status': 'Pending', 'days_ago': 0},
    {'username': 'carol', 'product': 'Multivitamin Complete', 'qty': 1, 'status': 'Pending', 'days_ago': 1},
    {'username': 'carol', 'product': 'Cetirizine 10mg', 'qty': 2, 'status': 'Delivered', 'days_ago': 21},
    {'username': 'dave', 'product': 'Metformin 500mg', 'qty': 2, 'status': 'Pending', 'days_ago': 0},
    {'username': 'dave', 'product': 'Amoxicillin 500mg', 'qty': 1, 'status': 'Shipped', 'days_ago': 7},
    {'username': 'alice', 'product': 'Omeprazole 20mg', 'qty': 1, 'status': 'Delivered', 'days_ago': 60},
    {'username': 'bob', 'product': 'Loratadine 10mg', 'qty': 2, 'status': 'Shipped', 'days_ago': 5},
]


def download_image(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=15)
        return resp.read()
    except Exception:
        return None


def seed():
    print('=== Seeding Products ===')
    Product.objects.all().delete()
    products = {}
    for data in PRODUCT_DATA:
        expiry = date.today() + timedelta(days=data['expiry_days'])
        product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock=data['stock'],
            expiry_date=expiry,
        )
        img_data = download_image(data['image_url'])
        if img_data:
            ext = data['image_url'].rsplit('.', 1)[-1].split('?')[0]
            filename = f'{data["name"].lower().replace(" ", "_").replace("/", "_")}.{ext}'
            product.image.save(filename, ContentFile(img_data), save=False)
        product.save()
        products[data['name']] = product
        print(f'  {data["name"]:25s} ${data["price"]:<5} stock={data["stock"]}')
    print(f'  → {len(PRODUCT_DATA)} products created\n')

    print('=== Seeding Users ===')
    User.objects.exclude(username='BikramGole').delete()
    users = {}
    for ud in USERS:
        if User.objects.filter(username=ud['username']).exists():
            user = User.objects.get(username=ud['username'])
        else:
            user = User.objects.create_user(
                username=ud['username'],
                password=ud['password'],
                is_staff=ud['is_staff'],
                is_superuser=ud['is_superuser'],
            )
        UserProfile.objects.update_or_create(
            user=user,
            defaults={'address': ud['address'], 'phone': ud['phone']},
        )
        users[ud['username']] = user
        staff = ' (staff)' if ud['is_staff'] else ''
        print(f'  {ud["username"]:15s}{staff}')
    print(f'  → {len(USERS)} users created\n')

    print('=== Seeding Orders ===')
    Order.objects.all().delete()
    for od in ORDERS:
        user = users.get(od['username'])
        product = products.get(od['product'])
        if not user or not product:
            print(f'  SKIP: {od["username"]} -> {od["product"]}')
            continue
        order_dt = timezone.make_aware(datetime.combine(
            date.today() - timedelta(days=od['days_ago']), datetime.min.time(),
        ))
        order = Order.objects.create(
            user=user,
            product=product,
            quantity=od['qty'],
            status=od['status'],
        )
        Order.objects.filter(pk=order.pk).update(order_date=order_dt)
        product.stock = max(0, product.stock - od['qty'])
        product.save(update_fields=['stock'])
        print(f'  {od["username"]:10s} → {od["qty"]}× {od["product"]:25s} [{od["status"]:10s}]')
    print(f'  → {len(ORDERS)} orders created\n')

    print('=== Summary ===')
    print(f'  Products: {Product.objects.count()}')
    print(f'  Users:    {User.objects.count()}')
    print(f'  Orders:   {Order.objects.count()}')
    print(f'  Profiles: {UserProfile.objects.count()}')
    print()
    print('Seeding complete. Run `python manage.py runserver` to start.')


if __name__ == '__main__':
    seed()
