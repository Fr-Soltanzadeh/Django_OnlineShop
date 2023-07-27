from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import CartView


class TestUrls(SimpleTestCase):
    def test_products(self):
        url = reverse("cart")
        self.assertEqual(resolve(url).func.view_class, CartView)
