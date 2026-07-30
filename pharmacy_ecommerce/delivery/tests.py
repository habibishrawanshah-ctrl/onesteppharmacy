from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order, OrderItem
from products.models import Product
from .models import Delivery, DeliveryZone


def create_user(username='testuser', password='testpass123'):
    return User.objects.create_user(username=username, password=password)


class DeliveryModelTest(TestCase):
    def setUp(self):
        user = create_user()
        product = Product.objects.create(name='Test Med', price=10, stock=100)
        self.order = Order.objects.create(user=user, total=10, shipping_address='addr', phone='123')
        OrderItem.objects.create(order=self.order, product=product, quantity=1, unit_price=10, total_price=10)

    def test_delivery_creation(self):
        d = Delivery.objects.create(
            order=self.order, user=self.order.user,
            address='addr', phone='123',
        )
        self.assertEqual(str(d), f'Delivery #{self.order.id} - pending')
        self.assertEqual(d.status, 'pending')

    def test_delivery_default_status(self):
        d = Delivery.objects.create(order=self.order, user=self.order.user, address='addr', phone='123')
        self.assertEqual(d.status, 'pending')

    def test_delivery_string_representation(self):
        d = Delivery(order=self.order, user=self.order.user, address='addr', phone='123', status='delivered')
        self.assertIn('delivered', str(d))

    def test_delivery_auto_timestamps(self):
        d = Delivery.objects.create(order=self.order, user=self.order.user, address='addr', phone='123')
        self.assertIsNotNone(d.created_at)
        self.assertIsNotNone(d.updated_at)

    def test_delivery_zone_creation(self):
        z = DeliveryZone.objects.create(name='Kathmandu Valley', districts='Kathmandu,Lalitpur,Bhaktapur', delivery_fee=50)
        self.assertEqual(str(z), 'Kathmandu Valley')
        self.assertEqual(z.delivery_fee, 50)

    def test_delivery_zone_free_threshold(self):
        z = DeliveryZone(min_order_free=500)
        self.assertEqual(z.min_order_free, 500)


class DeliveryViewTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client.login(username='testuser', password='testpass123')
        product = Product.objects.create(name='Test Med', price=10, stock=100)
        self.order = Order.objects.create(user=self.user, total=10, shipping_address='addr', phone='123')
        OrderItem.objects.create(order=self.order, product=product, quantity=1, unit_price=10, total_price=10)
        self.delivery = Delivery.objects.create(order=self.order, user=self.user, address='addr', phone='123', tracking_number='TRACK001')

    def test_my_deliveries_view(self):
        resp = self.client.get(reverse('delivery:my_deliveries'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'TRACK001')

    def test_tracking_view(self):
        resp = self.client.get(reverse('delivery:tracking', args=[self.delivery.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'pending')

    def test_my_deliveries_requires_auth(self):
        self.client.logout()
        resp = self.client.get(reverse('delivery:my_deliveries'))
        self.assertEqual(resp.status_code, 302)
