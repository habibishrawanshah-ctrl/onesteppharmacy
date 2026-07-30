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
        self.assertContains(resp, 'No products found')

    def test_stock_badge_in_stock(self):
        Product.objects.create(name='High', price=5.00, stock=100)
        resp = self.client.get(reverse('products:list'))
        self.assertContains(resp, 'in stock')

    def test_stock_badge_low_stock(self):
        Product.objects.create(name='Low', price=5.00, stock=5)
        resp = self.client.get(reverse('products:list'))
        self.assertContains(resp, 'Only 5 left')

    def test_stock_badge_out_of_stock(self):
        Product.objects.create(name='OOS', price=5.00, stock=0)
        resp = self.client.get(reverse('products:list'))
        self.assertContains(resp, 'Out of Stock')


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

    def test_buy_now_shown_when_auth_and_in_stock(self):
        create_user()
        self.client.login(username='tester', password='testpass123')
        resp = self.client.get(reverse('products:detail', args=[self.product.pk]))
        self.assertContains(resp, 'Buy Now')

    def test_add_to_cart_shown_on_detail(self):
        resp = self.client.get(reverse('products:detail', args=[self.product.pk]))
        self.assertContains(resp, 'Add to Cart')

    def test_buy_now_hidden_when_oos_and_auth(self):
        create_user()
        self.client.login(username='tester', password='testpass123')
        self.product.stock = 0
        self.product.save()
        resp = self.client.get(reverse('products:detail', args=[self.product.pk]))
        self.assertNotContains(resp, 'Buy Now')

    def test_out_of_stock_shown_when_oos(self):
        self.product.stock = 0
        self.product.save()
        resp = self.client.get(reverse('products:detail', args=[self.product.pk]))
        self.assertContains(resp, 'Out of Stock')
