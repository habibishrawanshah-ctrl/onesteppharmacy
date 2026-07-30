from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order
from .models import Payment, PaymentMethod


def create_user(username='testuser', password='testpass123'):
    return User.objects.create_user(username=username, password=password)


class PaymentMethodModelTest(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_create_payment_method(self):
        m = PaymentMethod.objects.create(
            user=self.user, method_type='khalti',
            account_name='Test User', account_number='9801234567',
        )
        self.assertIn('Khalti', str(m))
        self.assertEqual(m.method_type, 'khalti')

    def test_default_payment_method(self):
        m = PaymentMethod.objects.create(user=self.user, method_type='esewa')
        m2 = PaymentMethod.objects.create(user=self.user, method_type='bank_transfer', is_default=True)
        self.assertFalse(m.is_default)
        self.assertTrue(m2.is_default)

    def test_payment_method_ordering(self):
        m1 = PaymentMethod.objects.create(user=self.user, method_type='cash_on_delivery', is_default=False)
        m2 = PaymentMethod.objects.create(user=self.user, method_type='khalti', is_default=True)
        qs = PaymentMethod.objects.all()
        self.assertEqual(qs.first(), m2)


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.order = Order.objects.create(user=self.user, total=100, shipping_address='addr', phone='123')
        PaymentMethod.objects.create(user=self.user, method_type='cash_on_delivery')

    def test_create_payment(self):
        p = Payment.objects.create(
            order=self.order, user=self.user, amount=100,
            method_type='cash_on_delivery', status='pending',
        )
        self.assertIn(str(self.order.id), str(p))
        self.assertEqual(p.status, 'pending')

    def test_payment_default_pending(self):
        p = Payment.objects.create(
            order=self.order, user=self.user, amount=100, method_type='cash_on_delivery',
        )
        self.assertEqual(p.status, 'pending')

    def test_payment_completed(self):
        p = Payment.objects.create(
            order=self.order, user=self.user, amount=100,
            method_type='khalti', status='completed', transaction_id='TXN123',
        )
        self.assertEqual(p.transaction_id, 'TXN123')


class PaymentViewTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client.login(username='testuser', password='testpass123')
        self.order = Order.objects.create(user=self.user, total=100, shipping_address='addr', phone='123')
        self.method = PaymentMethod.objects.create(user=self.user, method_type='cash_on_delivery')
        self.payment = Payment.objects.create(
            order=self.order, user=self.user, amount=100,
            method_type='cash_on_delivery', status='pending',
        )

    def test_payment_methods_view(self):
        resp = self.client.get(reverse('payments:methods'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Cash on Delivery')

    def test_make_payment_view(self):
        resp = self.client.get(reverse('payments:make_payment', args=[self.order.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_make_payment_requires_auth(self):
        self.client.logout()
        resp = self.client.get(reverse('payments:make_payment', args=[self.order.pk]))
        self.assertEqual(resp.status_code, 302)
