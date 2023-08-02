from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import HomeView
from ..api_views import HomeApiView


class TestUrls(SimpleTestCase):
    def test_home(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_home_api(self):
        url = reverse("home_api")
        self.assertEqual(resolve(url).func.view_class, HomeApiView)
