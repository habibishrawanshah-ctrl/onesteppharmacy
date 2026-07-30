from django.core.management.base import BaseCommand
from products.models import Product, Category


PRODUCTS = [
    # Blood Glucose Monitors & Test Strips
    ("Apollo Pharmacy Smart Blood Glucose Monitoring Bluetooth System APG-01 + 25 Test Strips", 674, "Smart Bluetooth glucometer kit with 25 test strips and diabetes management app", 50),
    ("FreeStyle Libre Sensor - Flash Glucose Monitoring System 1 Count", 4438, "Flash glucose monitoring sensor for continuous glucose tracking", 30),
    ("Dr.Morepen Gluco One BG-03 Blood Glucose Test Strips 50 Count", 596, "Blood glucose test strips compatible with BG-03 glucometer", 100),
    ("Apollo Pharmacy Blood Glucose Test Strips 50 Count", 674, "Blood glucose test strips for Apollo Pharmacy glucometers", 100),
    ("Accu-Chek Instant Blood Glucose Test Strips 50 Count", 981, "Instant blood glucose test strips for Accu-Chek meters", 100),
    ("Accu-Chek Active Test Strips 50 Count", 948, "Blood glucose test strips for Accu-Chek Active meters", 100),
    ("Accu-Chek Active Test Strips 100 Count Value Pack", 1809, "Value pack of 100 blood glucose test strips", 80),
    ("Contour Plus Blood Glucose Test Strips 50 Count", 991, "Blood glucose test strips for Contour Plus meters", 90),
    ("OneTouch Select Plus Test Strips 50 Count", 1139, "Blood glucose test strips for OneTouch Select Plus meters", 90),
    ("OneTouch Verio Test Strips 50 Count", 1187, "Blood glucose test strips for OneTouch Verio meters", 85),
    ("OneTouch Select Test Strips 50 Count", 1117, "Blood glucose test strips for OneTouch Select meters", 85),
    ("Dr.Morepen Gluco One BG-03 Blood Glucose Test Strips 25 Count", 465, "Blood glucose test strips 25 pack for BG-03", 120),
    ("Dr.Morepen Gluco One Blood Glucose Monitoring System BG-03 With 25 Free Strips", 515, "Complete glucometer kit with 25 free test strips", 40),
    ("Accu-Chek Active Blood Glucose Monitoring System With 10 Free Strips", 922, "Complete blood glucose monitoring system with 10 test strips", 35),

    # BP Monitors
    ("Omron Blood Pressure Monitor HEM-7121 J", 1737, "Automatic blood pressure monitor for accurate readings", 45),
    ("Dr.Morepen Blood Pressure Monitor BP-15", 956, "Digital blood pressure monitor with large display", 50),
    ("Dr.Morepen BP One Blood Pressure Monitor BP-14", 1313, "Automatic blood pressure monitor with irregular heartbeat detection", 40),

    # Thermometers
    ("Apollo Pharmacy Non-Contact Infrared Thermometer", 832, "Non-contact infrared thermometer for fever screening", 60),
    ("Apollo Pharmacy Digital Thermometer", 120, "Digital thermometer for accurate body temperature", 100),

    # Nebulizers
    ("Apollo Pharmacy Compressor Nebulizer", 1434, "Compressor nebulizer for respiratory treatments", 30),
    ("Apollo Pharmacy Steam Inhaler Vaporizer", 291, "Steam inhaler for congestion and respiratory relief", 70),

    # Pulse Oximeters
    ("Apollo Pharmacy Pulse Oximeter", 1200, "Fingertip pulse oximeter for SpO2 and pulse rate", 55),
    ("Dr.Morepen Pulse Oximeter", 1500, "Digital fingertip pulse oximeter", 50),
    ("Omron Pulse Oximeter", 2200, "Premium pulse oximeter with accurate readings", 35),

    # Pregnancy & Ovulation Kits
    ("Prega News Pregnancy Test Kit 1 Count", 60, "Home pregnancy test kit - 99% accurate", 200),
    ("Prega News Advance Rapid Single-Step Pregnancy Test Kit", 120, "Advanced rapid pregnancy test kit", 150),
    ("Apollo Pharmacy LH Ovulation 5 Day Test Kit", 421, "Ovulation test kit for tracking fertility window", 80),
    ("i-know Ovulation Testing Strip 5 Count", 515, "Ovulation prediction test strips", 80),

    # Weighing Machines
    ("Apollo Pharmacy Digital Weighing Scale", 1800, "Digital weighing machine with tempered glass platform", 40),
    ("Omron Digital Weighing Scale HN-289", 2200, "Body weight scale with large LCD display", 35),
    ("Dr.Morepen Digital Weighing Scale", 1500, "Digital personal weighing scale", 45),

    # Supports & Splints
    ("Apollo Pharmacy Knee Support Adjustable", 350, "Adjustable knee support for injury recovery", 60),
    ("Apollo Pharmacy Lumbar Support Belt", 450, "Lumbar support belt for back pain relief", 55),
    ("Apollo Pharmacy Cervical Collar Neck Support", 300, "Soft cervical collar for neck support", 50),
    ("Apollo Pharmacy Wrist Support Brace", 280, "Wrist support brace for sprains and strains", 55),
    ("Apollo Pharmacy Ankle Support Brace", 320, "Ankle support brace for injury prevention", 50),
    ("Apollo Pharmacy Abdominal Support Belt", 400, "Abdominal support belt for post-surgery recovery", 45),
    ("Apollo Pharmacy Clavicle Support", 380, "Clavicle support brace for shoulder injuries", 35),
    ("Apollo Pharmacy Arm Sling", 250, "Adjustable arm sling for arm support", 60),

    # Health Accessories
    ("Apollo Pharmacy Ortho Slippers", 600, "Orthopedic slippers for foot comfort and support", 80),
    ("Apollo Pharmacy Heating Belt", 500, "Electric heating belt for pain relief", 40),
    ("Apollo Pharmacy Compression Gloves", 350, "Compression gloves for arthritis relief", 50),
    ("Apollo Pharmacy Neck Pillow Memory Foam", 450, "Memory foam neck pillow for travel and posture", 60),
    ("Apollo Pharmacy Face Mask Surgical 50 Pack", 250, "Disposable surgical face masks - pack of 50", 200),
    ("Apollo Pharmacy N95 Face Mask 10 Pack", 350, "N95 respirator masks - pack of 10", 150),
    ("Apollo Pharmacy Hand Sanitizer 500ml", 150, "Alcohol-based hand sanitizer 500ml bottle", 120),
    ("Apollo Pharmacy First Aid Kit", 400, "Comprehensive first aid kit for home and travel", 70),
    ("Apollo Pharmacy Hot Water Bag", 250, "Rubber hot water bag for pain relief", 80),
    ("Apollo Pharmacy Walking Stick Aluminum", 600, "Adjustable aluminum walking stick", 40),

    # Testing Kits
    ("Apollo Pharmacy COVID-19 Rapid Antigen Test Kit", 250, "Rapid antigen test kit for COVID-19 detection", 100),
    ("Apollo Pharmacy Vitamin D Test Kit", 500, "At-home vitamin D testing kit", 40),
    ("Apollo Pharmacy Thyroid Test Kit", 550, "At-home thyroid function test kit", 35),
    ("Apollo Pharmacy Lipid Profile Test Kit", 600, "At-home lipid profile testing kit", 35),
]


class Command(BaseCommand):
    help = 'Seed database with health device products from Apollo Pharmacy catalogue'

    def handle(self, *args, **options):
        cat, created = Category.objects.get_or_create(name='Health Devices', slug='health-devices')
        if created:
            self.stdout.write(f'Created category: {cat.name}')

        existing = Product.objects.filter(category=cat).count()
        imported = 0
        for name, price, desc, stock in PRODUCTS:
            _, was_created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': cat,
                    'description': desc,
                    'price': price,
                    'stock': stock,
                    'manufacturer': 'Apollo Pharmacy',
                }
            )
            if was_created:
                imported += 1

        self.stdout.write(self.style.SUCCESS(
            f'Category had {existing} existing products. Imported {imported} new products. '
            f'Total: {Product.objects.filter(category=cat).count()}'
        ))
