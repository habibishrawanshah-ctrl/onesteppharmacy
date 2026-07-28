import os
import sys
import django
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_ecommerce.settings')
django.setup()

from django.core.files.base import ContentFile
import urllib.request
from products.models import Product

PRODUCTS = [
    {
        'name': 'Paracetamol 500mg',
        'description': 'Effective pain reliever and fever reducer. Used for headaches, muscle aches, arthritis, backache, toothaches, colds, and fevers. Each tablet contains 500mg of paracetamol.',
        'price': 4.99,
        'stock': 150,
        'expiry_days': 730,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/a/a5/Medication_Paracetamol.JPG',
    },
    {
        'name': 'Ibuprofen 200mg',
        'description': 'Nonsteroidal anti-inflammatory drug (NSAID) used for relief of fever, mild to moderate pain, and inflammation. Ideal for headaches, menstrual cramps, toothache, and back pain.',
        'price': 6.99,
        'stock': 200,
        'expiry_days': 730,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/b/b0/200mg_ibuprofen_tablets.jpg',
    },
    {
        'name': 'Amoxicillin 500mg',
        'description': 'Broad-spectrum penicillin antibiotic used to treat bacterial infections including respiratory tract infections, ear infections, skin infections, and urinary tract infections.',
        'price': 12.99,
        'stock': 80,
        'expiry_days': 365,
        'image_url': 'https://images.pexels.com/photos/3683073/pexels-photo-3683073.jpeg',
    },
    {
        'name': 'Vitamin C 1000mg',
        'description': 'High-strength vitamin C supplement to support immune system function, collagen production, and antioxidant protection. Each tablet provides 1000mg of ascorbic acid.',
        'price': 9.99,
        'stock': 120,
        'expiry_days': 1095,
        'image_url': 'https://images.pexels.com/photos/4047077/pexels-photo-4047077.jpeg',
    },
    {
        'name': 'Omeprazole 20mg',
        'description': 'Proton pump inhibitor (PPI) used to treat gastroesophageal reflux disease (GERD), stomach ulcers, and other conditions caused by excess stomach acid.',
        'price': 14.99,
        'stock': 90,
        'expiry_days': 730,
        'image_url': 'https://images.pexels.com/photos/3873149/pexels-photo-3873149.jpeg',
    },
    {
        'name': 'Cetirizine 10mg',
        'description': 'Antihistamine medication used to relieve allergy symptoms such as watery eyes, runny nose, itching eyes/nose, sneezing, and hives. 24-hour non-drowsy relief.',
        'price': 8.99,
        'stock': 100,
        'expiry_days': 730,
        'image_url': 'https://images.pexels.com/photos/9742778/pexels-photo-9742778.jpeg',
    },
    {
        'name': 'Aspirin 81mg',
        'description': 'Low-dose aspirin for cardiovascular protection. Also used as a mild pain reliever and fever reducer. Enteric-coated for gentle on the stomach.',
        'price': 5.49,
        'stock': 180,
        'expiry_days': 1095,
        'image_url': 'https://images.pexels.com/photos/51929/medications-cure-tablets-pharmacy-51929.jpeg',
    },
    {
        'name': 'Multivitamin Complete',
        'description': 'Complete daily multivitamin and mineral supplement with vitamins A, C, D, E, B-complex, zinc, iron, and calcium. Supports overall health and fills nutritional gaps.',
        'price': 15.99,
        'stock': 60,
        'expiry_days': 1095,
        'image_url': 'https://images.pexels.com/photos/5452239/pexels-photo-5452239.jpeg',
    },
    {
        'name': 'Metformin 500mg',
        'description': 'First-line medication for type 2 diabetes. Helps control blood sugar levels by improving insulin sensitivity and reducing glucose production in the liver.',
        'price': 7.99,
        'stock': 110,
        'expiry_days': 730,
        'image_url': 'https://images.pexels.com/photos/7526049/pexels-photo-7526049.jpeg',
    },
    {
        'name': 'Loratadine 10mg',
        'description': 'Non-drowsy antihistamine for seasonal allergy relief. Provides 24-hour relief from sneezing, runny nose, itchy eyes, and throat irritation.',
        'price': 7.49,
        'stock': 130,
        'expiry_days': 730,
        'image_url': 'https://images.pexels.com/photos/9742893/pexels-photo-9742893.jpeg',
    },
]

def download_image(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=15)
        return resp.read()
    except Exception as e:
        print(f'  Failed: {e}')
        return None

def seed():
    Product.objects.filter(image='').delete()
    Product.objects.filter(image__isnull=True).delete()

    created = 0
    for data in PRODUCTS:
        name = data['name']
        if Product.objects.filter(name=name).exists():
            print(f'  Skipping {name} (already exists)')
            continue

        expiry = date.today() + timedelta(days=data['expiry_days'])
        product = Product(
            name=name,
            description=data['description'],
            price=data['price'],
            stock=data['stock'],
            expiry_date=expiry,
        )

        img_data = download_image(data['image_url'])
        if img_data:
            ext = data['image_url'].rsplit('.', 1)[-1].split('?')[0]
            filename = f'{name.lower().replace(" ", "_").replace("/", "_")}.{ext}'
            product.image.save(filename, ContentFile(img_data), save=False)
            print(f'  Image: OK')
        else:
            print(f'  Image: none')

        product.save()
        created += 1
        print(f'  Created: {name} — ${data["price"]} | Stock: {data["stock"]}')

    print(f'\nDone! {created} products created.')

if __name__ == '__main__':
    seed()
