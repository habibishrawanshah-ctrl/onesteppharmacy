from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import InsuranceProvider, UserInsurance


def create_user(username='testuser', password='testpass123'):
    return User.objects.create_user(username=username, password=password)


class InsuranceProviderModelTest(TestCase):
    def test_create_provider(self):
        p = InsuranceProvider.objects.create(name='United Health', contact_phone='1234567890')
        self.assertEqual(str(p), 'United Health')
        self.assertTrue(p.is_active)

    def test_provider_default_active(self):
        p = InsuranceProvider.objects.create(name='BlueCross')
        self.assertTrue(p.is_active)

    def test_provider_inactive(self):
        p = InsuranceProvider.objects.create(name='Old Provider', is_active=False)
        self.assertFalse(p.is_active)


class UserInsuranceModelTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.provider = InsuranceProvider.objects.create(name='Aetna')

    def test_create_user_insurance(self):
        u = UserInsurance.objects.create(
            user=self.user, provider=self.provider,
            policy_number='POL123', coverage_type='premium',
        )
        self.assertIn('POL123', str(u))
        self.assertEqual(u.coverage_type, 'premium')

    def test_insurance_default_basic(self):
        u = UserInsurance.objects.create(
            user=self.user, provider=self.provider, policy_number='POL456',
        )
        self.assertEqual(u.coverage_type, 'basic')

    def test_insurance_unique_policy(self):
        UserInsurance.objects.create(user=self.user, provider=self.provider, policy_number='POL999')
        with self.assertRaises(Exception):
            UserInsurance.objects.create(user=self.user, provider=self.provider, policy_number='POL999')


class InsuranceViewTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client.login(username='testuser', password='testpass123')
        self.provider = InsuranceProvider.objects.create(name='Cigna')
        UserInsurance.objects.create(user=self.user, provider=self.provider, policy_number='P789')

    def test_my_insurance_view(self):
        resp = self.client.get(reverse('insurance:my_insurance'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Cigna')

    def test_my_insurance_requires_auth(self):
        self.client.logout()
        resp = self.client.get(reverse('insurance:my_insurance'))
        self.assertEqual(resp.status_code, 302)
