from django.test import TestCase
from django.urls import reverse
from .models import Product
from django.contrib.auth.models import User


def create_user():
    return User.objects.create_user(username='tester', password='testpass123')


class ProductModelTest(TestCase):
    def test_string_representation(self):
        p = Product.objects.create(name='Test Med', price=9.99, stock=50)
        self.assertEqual(str(p), 'Test Med')

    def test_default_stock(self):
        p = Product.objects.create(name='No Stock', price=5.00)
        self.assertEqual(p.stock, 0)


class ProductListViewTest(TestCase):
    def setUp(self):
        for i in range(3):
            Product.objects.create(name=f'Product {i}', price=i + 1.00, stock=10)

    def test_list_all_products(self):
        resp = self.client.get(reverse('products:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Product 0')

    def test_empty_list_shows_message(self):
        Product.objects.all().delete()
        resp = self.client.get(reverse('products:list'))
        self.assertContains(resp, 'No products available')

    def test_stock_badge_in_stock(self):
        Product.objects.create(name='High', price=5.00, stock=100)
        resp = self.client.get(reverse('products:list'))
        self.assertContains(resp, '100 in stock')

    def test_stock_badge_low_stock(self):
        Product.objects.create(name='Low', price=5.00, stock=5)
        resp = self.client.get(reverse('products:list'))
        self.assertContains(resp, 'Only 5 left')

    def test_stock_badge_out_of_stock(self):
        Product.objects.create(name='OOS', price=5.00, stock=0)
        resp = self.client.get(reverse('products:list'))
        self.assertContains(resp, 'Out of Stock')

    def test_expiry_badge_hidden_when_null_on_list(self):
        Product.objects.create(name='NoExp', price=5.00, stock=10, expiry_date=None)
        resp = self.client.get(reverse('products:list'))
        self.assertNotContains(resp, 'Exp:')


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Detail Test', description='Desc', price=9.99, stock=10,
        )

    def test_detail_page_renders(self):
        resp = self.client.get(reverse('products:detail', args=[self.product.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Detail Test')

    def test_404_for_missing_product(self):
        resp = self.client.get(reverse('products:detail', args=[9999]))
        self.assertEqual(resp.status_code, 404)

    def test_place_order_shown_when_auth_and_in_stock(self):
        create_user()
        self.client.login(username='tester', password='testpass123')
        resp = self.client.get(reverse('products:detail', args=[self.product.pk]))
        self.assertContains(resp, 'Place Order')

    def test_login_to_order_shown_when_anonymous_and_in_stock(self):
        resp = self.client.get(reverse('products:detail', args=[self.product.pk]))
        self.assertContains(resp, 'Login to Order')

    def test_place_order_hidden_when_oos_and_auth(self):
        create_user()
        self.client.login(username='tester', password='testpass123')
        self.product.stock = 0
        self.product.save()
        resp = self.client.get(reverse('products:detail', args=[self.product.pk]))
        self.assertNotContains(resp, 'Place Order')

    def test_login_to_order_hidden_when_oos(self):
        self.product.stock = 0
        self.product.save()
        resp = self.client.get(reverse('products:detail', args=[self.product.pk]))
        self.assertNotContains(resp, 'Login to Order')

    def test_expiry_hidden_when_no_expiry(self):
        self.product.expiry_date = None
        self.product.save()
        resp = self.client.get(reverse('products:detail', args=[self.product.pk]))
        self.assertNotContains(resp, '<strong>Expiry:</strong>')

    def test_back_to_products_link_shown(self):
        resp = self.client.get(reverse('products:detail', args=[self.product.pk]))
        self.assertContains(resp, 'Back to Products')
