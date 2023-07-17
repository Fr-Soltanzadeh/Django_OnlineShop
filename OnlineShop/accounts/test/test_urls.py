from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import LoginView, LogoutView


class TestUrls(SimpleTestCase):
    def test_login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)