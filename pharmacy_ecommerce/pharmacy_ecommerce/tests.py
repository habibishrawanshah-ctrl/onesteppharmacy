from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings


class AboutPageTest(TestCase):
    def test_about_page_returns_200(self):
        resp = self.client.get(reverse('about'))
        self.assertEqual(resp.status_code, 200)

    def test_about_page_has_company_name(self):
        resp = self.client.get(reverse('about'))
        self.assertContains(resp, 'OneStep')

    def test_about_page_has_3d_viewer(self):
        resp = self.client.get(reverse('about'))
        self.assertContains(resp, 'model-viewer')

    def test_about_page_has_team_section(self):
        resp = self.client.get(reverse('about'))
        self.assertContains(resp, 'Our Team')

    def test_about_page_has_stats(self):
        resp = self.client.get(reverse('about'))
        self.assertContains(resp, '500+')

    def test_about_page_accessible_to_anonymous(self):
        resp = self.client.get(reverse('about'))
        self.assertEqual(resp.status_code, 200)


class SecuritySettingsTest(TestCase):
    def test_content_type_nosniff_enabled(self):
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)

    def test_xss_filter_enabled(self):
        self.assertTrue(settings.SECURE_BROWSER_XSS_FILTER)

    def test_x_frame_options_deny(self):
        self.assertEqual(settings.X_FRAME_OPTIONS, 'DENY')

    def test_session_cookie_httponly(self):
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)

    def test_csrf_cookie_httponly(self):
        self.assertTrue(settings.CSRF_COOKIE_HTTPONLY)

    def test_session_cookie_samesite_lax(self):
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, 'Lax')

    def test_csrf_cookie_samesite_lax(self):
        self.assertEqual(settings.CSRF_COOKIE_SAMESITE, 'Lax')


class NavigationTest(TestCase):
    def test_anonymous_nav_shows_login_button(self):
        resp = self.client.get(reverse('home'))
        self.assertContains(resp, 'Log In')

    def test_anonymous_nav_shows_signup_button(self):
        resp = self.client.get(reverse('home'))
        self.assertContains(resp, 'Sign Up')

    def test_anonymous_nav_hides_logout(self):
        resp = self.client.get(reverse('home'))
        self.assertNotContains(resp, 'Logout')

    def test_authenticated_nav_shows_logout(self):
        from django.contrib.auth.models import User
        User.objects.create_user(username='navtest', password='pass1234')
        self.client.login(username='navtest', password='pass1234')
        resp = self.client.get(reverse('home'))
        self.assertContains(resp, 'Logout')

    def test_authenticated_nav_hides_signup(self):
        from django.contrib.auth.models import User
        User.objects.create_user(username='navtest2', password='pass1234')
        self.client.login(username='navtest2', password='pass1234')
        resp = self.client.get(reverse('home'))
        self.assertNotContains(resp, 'Sign Up')

    def test_staff_nav_shows_admin_link(self):
        from django.contrib.auth.models import User
        User.objects.create_user(username='stafftest', password='pass1234', is_staff=True)
        self.client.login(username='stafftest', password='pass1234')
        resp = self.client.get(reverse('home'))
        self.assertContains(resp, 'Admin')
