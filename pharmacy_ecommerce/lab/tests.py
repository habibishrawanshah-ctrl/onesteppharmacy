from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import LabTest, LabBooking
from django.utils import timezone


def create_user(username='testuser', password='testpass123'):
    return User.objects.create_user(username=username, password=password)


class LabTestModelTest(TestCase):
    def test_create_lab_test(self):
        t = LabTest.objects.create(name='CBC', price=500, category='blood')
        self.assertEqual(str(t), 'CBC')
        self.assertEqual(t.category, 'blood')

    def test_lab_test_default_active(self):
        t = LabTest.objects.create(name='X-Ray Chest', price=1200, category='imaging')
        self.assertTrue(t.is_active)

    def test_lab_test_inactive(self):
        t = LabTest.objects.create(name='Old Test', price=100, is_active=False)
        self.assertFalse(t.is_active)


class LabBookingModelTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.test = LabTest.objects.create(name='Lipid Profile', price=800)

    def test_create_booking(self):
        b = LabBooking.objects.create(
            user=self.user, lab_test=self.test,
            booking_date=timezone.now(), status='confirmed',
        )
        self.assertEqual(b.status, 'confirmed')
        self.assertIn('Lipid Profile', str(b))

    def test_booking_default_pending(self):
        b = LabBooking.objects.create(
            user=self.user, lab_test=self.test,
            booking_date=timezone.now(),
        )
        self.assertEqual(b.status, 'pending')

    def test_booking_address(self):
        b = LabBooking.objects.create(
            user=self.user, lab_test=self.test,
            booking_date=timezone.now(), address='123 Main St',
        )
        self.assertEqual(b.address, '123 Main St')


class LabViewTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client.login(username='testuser', password='testpass123')
        self.test = LabTest.objects.create(name='Thyroid Test', price=600)
        LabBooking.objects.create(
            user=self.user, lab_test=self.test,
            booking_date=timezone.now(),
        )

    def test_my_bookings_view(self):
        resp = self.client.get(reverse('lab:my_bookings'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Thyroid Test')

    def test_my_bookings_requires_auth(self):
        self.client.logout()
        resp = self.client.get(reverse('lab:my_bookings'))
        self.assertEqual(resp.status_code, 302)
