from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import LoginView, LogoutView, ProfileView


class TestUrls(SimpleTestCase):
    def test_login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_profile(self):
        url = reverse('profile', args=("1",))
        self.assertEqual(resolve(url).func.view_class, ProfileView)