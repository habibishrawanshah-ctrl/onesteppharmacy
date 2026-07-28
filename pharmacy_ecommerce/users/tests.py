from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile


class SignupViewTest(TestCase):
    def test_signup_page_renders(self):
        resp = self.client.get(reverse('users:signup'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Create Account')

    def test_signup_creates_user_and_profile(self):
        resp = self.client.post(reverse('users:signup'), {
            'username': 'newuser',
            'password1': 'Str0ng!Pass',
            'password2': 'Str0ng!Pass',
        })
        self.assertRedirects(resp, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_signup_duplicate_username_shows_error(self):
        User.objects.create_user(username='existing', password='pass1234')
        resp = self.client.post(reverse('users:signup'), {
            'username': 'existing',
            'password1': 'Str0ng!Pass',
            'password2': 'Str0ng!Pass',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'already exists')

    def test_signup_password_mismatch_shows_error(self):
        resp = self.client.post(reverse('users:signup'), {
            'username': 'testuser',
            'password1': 'pass1234',
            'password2': 'diffpass',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'didn\u2019t match')

    def test_signup_weak_password_shows_error(self):
        resp = self.client.post(reverse('users:signup'), {
            'username': 'testuser',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'too common')

    def test_signup_numeric_password_shows_error(self):
        resp = self.client.post(reverse('users:signup'), {
            'username': 'testuser',
            'password1': '12345678',
            'password2': '12345678',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'entirely numeric')


class UserProfileModelTest(TestCase):
    def test_create_profile(self):
        user = User.objects.create_user(username='profiled', password='pass1234')
        profile = UserProfile.objects.create(user=user, address='123 Main St', phone='555-0100')
        self.assertEqual(str(profile), 'profiled')
        self.assertEqual(profile.address, '123 Main St')
