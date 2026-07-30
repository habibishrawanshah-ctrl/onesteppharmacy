from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import HealthRecord, HealthCondition, BlogPost


def create_user(username='testuser', password='testpass123'):
    return User.objects.create_user(username=username, password=password)


class HealthConditionModelTest(TestCase):
    def test_create_condition(self):
        c = HealthCondition.objects.create(name='Diabetes', description='High blood sugar')
        self.assertEqual(str(c), 'Diabetes')

    def test_condition_common_medicines(self):
        c = HealthCondition.objects.create(name='Hypertension', common_medicines='Amlodipine,Lisinopril')
        self.assertIn('Amlodipine', c.common_medicines)


class HealthRecordModelTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.condition = HealthCondition.objects.create(name='Asthma')

    def test_create_health_record(self):
        r = HealthRecord.objects.create(user=self.user, condition=self.condition, notes='Use inhaler')
        self.assertIn('Asthma', str(r))

    def test_health_record_with_custom_condition(self):
        r = HealthRecord.objects.create(user=self.user, custom_condition='Rare Disease')
        self.assertIn('Rare Disease', str(r))

    def test_health_record_default_is_active(self):
        r = HealthRecord.objects.create(user=self.user, custom_condition='Test')
        self.assertTrue(r.is_active)

    def test_health_record_ordering(self):
        r1 = HealthRecord.objects.create(user=self.user, custom_condition='First')
        r2 = HealthRecord.objects.create(user=self.user, custom_condition='Second')
        qs = HealthRecord.objects.all()
        self.assertEqual(qs.first(), r2)


class HealthViewTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client.login(username='testuser', password='testpass123')
        self.condition = HealthCondition.objects.create(name='Allergy')
        HealthRecord.objects.create(user=self.user, condition=self.condition)

    def test_my_records_view(self):
        resp = self.client.get(reverse('health:my_records'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Allergy')

    def test_my_records_requires_auth(self):
        self.client.logout()
        resp = self.client.get(reverse('health:my_records'))
        self.assertEqual(resp.status_code, 302)


class BlogPostModelTest(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_create_blog_post(self):
        b = BlogPost.objects.create(title='Health Tips', slug='health-tips', content='Stay healthy!', author=self.user)
        self.assertEqual(str(b), 'Health Tips')

    def test_blog_post_default_published(self):
        b = BlogPost.objects.create(title='Wellness', slug='wellness', content='Be well', author=self.user)
        self.assertTrue(b.is_published)

    def test_blog_post_draft(self):
        b = BlogPost.objects.create(title='Draft', slug='draft', content='Draft post', author=self.user, is_published=False)
        self.assertFalse(b.is_published)


class BlogViewTest(TestCase):
    def setUp(self):
        self.user = create_user()
        BlogPost.objects.create(title='Article One', slug='article-one', content='Content one', author=self.user, category='Wellness')
        BlogPost.objects.create(title='Article Two', slug='article-two', content='Content two', author=self.user, category='Nutrition')

    def test_blog_list_view(self):
        resp = self.client.get(reverse('health:blog_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Article One')

    def test_blog_detail_view(self):
        resp = self.client.get(reverse('health:blog_detail', args=['article-one']))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Content one')

    def test_blog_detail_404(self):
        resp = self.client.get(reverse('health:blog_detail', args=['nonexistent']))
        self.assertEqual(resp.status_code, 404)

    def test_blog_category_filter(self):
        resp = self.client.get(reverse('health:blog_list') + '?category=Nutrition')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Article Two')
        self.assertNotContains(resp, 'Article One')

    def test_blog_rss_feed(self):
        resp = self.client.get(reverse('health:blog_feed'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Article One')
