from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import LoginOrRegisterView, LogoutView, ProfileView, VerifyCodeView
from accounts.api.views import (
    LoginOrRegisterApiView,
    CustomerApiView,
    VerifyCodeApiView,
)


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
        url = reverse("profile")
        self.assertEqual(resolve(url).func.view_class, ProfileView)

    def test_login(self):
        url = reverse("login_api")
        self.assertEqual(resolve(url).func.view_class, LoginOrRegisterApiView)

    def test_verify_code(self):
        url = reverse("verify_code_api")
        self.assertEqual(resolve(url).func.view_class, VerifyCodeApiView)

    def test_profile(self):
        url = reverse("profile_api")
        self.assertEqual(resolve(url).func.view_class, CustomerApiView)
