from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..views import CartView


class TestCartView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_Cart_GET(self):
        response = self.client.get(reverse("cart"))
        self.assertTemplateUsed(response, "cart/cart.html")
        self.assertEqual(response.status_code, 200)
