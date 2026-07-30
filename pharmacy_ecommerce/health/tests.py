from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import HealthRecord, HealthCondition


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
