from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import LoginOrRegisterView, LogoutView, ProfileView, VerifyCodeView


class TestUrls(SimpleTestCase):
    def test_login(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func.view_class, LoginOrRegisterView)

    def test_verify_code(self):
        url = reverse("verify_code")
        self.assertEqual(resolve(url).func.view_class, VerifyCodeView)

    def test_logout(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_profile(self):
        url = reverse("profile", args=("1",))
        self.assertEqual(resolve(url).func.view_class, ProfileView)
