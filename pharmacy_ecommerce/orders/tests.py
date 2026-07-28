from django.test import TestCase
from django.urls import reverse
from .models import Order
from products.models import Product
from django.contrib.auth.models import User


def create_user():
    return User.objects.create_user(username='buyer', password='pass1234')


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.product = Product.objects.create(name='Test', price=5.00, stock=10)

    def test_string_representation(self):
        order = Order.objects.create(user=self.user, product=self.product, quantity=2)
        self.assertIn('buyer', str(order))

    def test_default_status_is_pending(self):
        order = Order.objects.create(user=self.user, product=self.product, quantity=1)
        self.assertEqual(order.status, 'Pending')


class PlaceOrderViewTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.product = Product.objects.create(
            name='Painkiller', description='Effective', price=4.99, stock=10,
        )

    def test_login_required(self):
        resp = self.client.get(reverse('orders:place', args=[self.product.pk]))
        self.assertRedirects(resp, f'/login/?next=/orders/place/{self.product.pk}/')

    def test_place_order_success(self):
        self.client.login(username='buyer', password='pass1234')
        resp = self.client.post(
            reverse('orders:place', args=[self.product.pk]),
            {'quantity': 3},
        )
        self.assertRedirects(resp, reverse('orders:success'))
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.quantity, 3)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)

    def test_decrements_stock(self):
        self.client.login(username='buyer', password='pass1234')
        self.client.post(
            reverse('orders:place', args=[self.product.pk]),
            {'quantity': 3},
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)

    def test_rejects_quantity_exceeding_stock(self):
        self.client.login(username='buyer', password='pass1234')
        resp = self.client.post(
            reverse('orders:place', args=[self.product.pk]),
            {'quantity': 999},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Only 10 in stock')
        self.assertEqual(Order.objects.count(), 0)

    def test_rejects_zero_quantity(self):
        self.client.login(username='buyer', password='pass1234')
        resp = self.client.post(
            reverse('orders:place', args=[self.product.pk]),
            {'quantity': 0},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Quantity must be at least 1')
        self.assertEqual(Order.objects.count(), 0)

    def test_rejects_negative_quantity(self):
        self.client.login(username='buyer', password='pass1234')
        resp = self.client.post(
            reverse('orders:place', args=[self.product.pk]),
            {'quantity': -5},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Quantity must be at least 1')
        self.assertEqual(Order.objects.count(), 0)

    def test_rejects_non_numeric_quantity(self):
        self.client.login(username='buyer', password='pass1234')
        resp = self.client.post(
            reverse('orders:place', args=[self.product.pk]),
            {'quantity': 'abc'},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Quantity must be a whole number')
        self.assertEqual(Order.objects.count(), 0)

    def test_rejects_missing_quantity(self):
        self.client.login(username='buyer', password='pass1234')
        resp = self.client.post(
            reverse('orders:place', args=[self.product.pk]),
            {},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Quantity must be a whole number')
        self.assertEqual(Order.objects.count(), 0)

    def test_404_for_nonexistent_product(self):
        self.client.login(username='buyer', password='pass1234')
        resp = self.client.post(
            reverse('orders:place', args=[9999]),
            {'quantity': 1},
        )
        self.assertEqual(resp.status_code, 404)

    def test_get_form_shows_product_details(self):
        self.client.login(username='buyer', password='pass1234')
        resp = self.client.get(reverse('orders:place', args=[self.product.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Painkiller')
        self.assertContains(resp, '4.99')
        self.assertContains(resp, 'max="10"')


class PlaceOrderIndexTest(TestCase):
    def test_redirects_to_product_list(self):
        resp = self.client.get(reverse('orders:place_index'))
        self.assertRedirects(resp, reverse('products:list'))


class SuccessViewTest(TestCase):
    def test_success_page_renders(self):
        resp = self.client.get(reverse('orders:success'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Order Placed Successfully')
