from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from .models import Review


def create_user(username='testuser', password='testpass123'):
    return User.objects.create_user(username=username, password=password)


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.product = Product.objects.create(name='Test Med', price=9.99)

    def test_create_review(self):
        r = Review.objects.create(user=self.user, product=self.product, rating=5, comment='Great!')
        self.assertEqual(r.rating, 5)
        self.assertIn('5★', str(r))

    def test_review_unique_user_product(self):
        Review.objects.create(user=self.user, product=self.product, rating=4)
        with self.assertRaises(Exception):
            Review.objects.create(user=self.user, product=self.product, rating=3)

    def test_review_min_rating(self):
        r = Review.objects.create(user=self.user, product=self.product, rating=1)
        self.assertEqual(r.rating, 1)

    def test_review_max_rating(self):
        r = Review.objects.create(user=self.user, product=self.product, rating=5)
        self.assertEqual(r.rating, 5)

    def test_review_blank_comment_allowed(self):
        r = Review.objects.create(user=self.user, product=self.product, rating=3)
        self.assertEqual(r.comment, '')

    def test_review_string_representation(self):
        r = Review.objects.create(user=self.user, product=self.product, rating=4, comment='Nice')
        self.assertIn('Test Med', str(r))


class ReviewViewTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.product = Product.objects.create(name='Paracetamol', price=5.00, stock=100)
        self.client.login(username='testuser', password='testpass123')

    def test_add_review(self):
        resp = self.client.post(reverse('reviews:add', args=[self.product.pk]), {
            'rating': 5, 'comment': 'Excellent!',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Review.objects.filter(product=self.product, user=self.user).exists())

    def test_add_review_requires_login(self):
        self.client.logout()
        resp = self.client.post(reverse('reviews:add', args=[self.product.pk]), {
            'rating': 4, 'comment': 'Good',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Review.objects.filter(product=self.product).exists())
