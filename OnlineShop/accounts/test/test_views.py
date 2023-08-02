from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..forms import LoginForm, VerifyCodeForm
from ..models import User


class TestLoginOrRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_GET(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context["form"], LoginForm)


class TestVerifyCodeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(phone_number="09102098929", password="123")
        self.client.post(reverse("login_api"), data={"phone_number": "09102098929"})
        self.client.session.save()

    def test_get_authenticated_user_redirected_to_profile(self):
        self.client.login(username="09102098929", password="123")
        self.assertTrue(self.client.session.get('_auth_user_id'))
        response = self.client.get(reverse('verify_code'))
        self.assertRedirects(response, reverse('profile'))

    def test_get_unauthenticated_user_redirected_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('verify_code'))
        self.assertRedirects(response, reverse('login'))

    def test_VerifyCode_GET(self):
        self.client.logout()
        self.client.session['login_info'] = {
                    "phone_number": "09102098929",
                    "redirect_to": "",
                }
        self.client.session.save()
        response = self.client.get(reverse("verify_code"))       
        # self.assertTemplateUsed(response, "accounts/verify_code.html")
        # self.assertEqual(response.status_code, 200)
        # self.failUnless(response.context["form"], VerifyCodeForm)


class TestLogoutView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(phone_number="09102098929", password="123")

    def test_logout_GET(self):
        self.client.login(username="09102098929", password="123")
        self.assertTrue(self.client.session.get('_auth_user_id'))
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.session.get('_auth_user_id'))
        self.assertRedirects(response, reverse('login'))


class TestProfileView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_profile_GET(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
