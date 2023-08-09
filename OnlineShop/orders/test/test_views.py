from django.test import TestCase, RequestFactory, Client
from django.urls import reverse


class TestCheckoutView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_Checkout_GET(self):
        response = self.client.get(reverse("checkout"))
        self.assertTemplateUsed(response, "orders/checkout.html")
        self.assertEqual(response.status_code, 200)
