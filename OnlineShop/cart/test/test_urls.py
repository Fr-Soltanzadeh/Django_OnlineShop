from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import CartView
from ..api_views import CartApiView, AddToCartApiView


class TestUrls(SimpleTestCase):
    def test_cart(self):
        url = reverse("cart")
        self.assertEqual(resolve(url).func.view_class, CartView)

    def test_add_to_cart_api(self):
        url = reverse("cart_api")
        self.assertEqual(resolve(url).func.view_class, CartApiView)

    def test_add_to_cart_api(self):
        url = reverse("add_to_cart_api")
        self.assertEqual(resolve(url).func.view_class, AddToCartApiView)
