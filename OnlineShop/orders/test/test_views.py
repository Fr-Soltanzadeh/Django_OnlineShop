from django.test import TestCase, RequestFactory, Client
from model_bakery import baker
from django.urls import reverse
from decimal import Decimal
from accounts.models import User, Customer
from ..models import Order
from ..views import VerifyOrderView, OrderPayView
from rest_framework import status


class TestCheckoutView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_Checkout_GET(self):
        response = self.client.get(reverse("checkout"))
        self.assertTemplateUsed(response, "orders/checkout.html")
        self.assertEqual(response.status_code, 200)


class TestPayView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(phone_number="09102098929")
        self.order = baker.make(
            Order,
            customer=self.user,
            total_price=Decimal(10.00),
            final_price=Decimal(10.00),
        )
        self.view = OrderPayView.as_view()
        self.url = reverse("pay", args=(self.order.id,))

    def test_Pay_GET(self):
        request = self.factory.get(self.url)
        request.user = self.user
        request.session = {}
        response = self.view(request, order_id=self.order.id)
        self.assertEqual(response.status_code, 302)


class TestVerifyOrderView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.customer = Customer.objects.create(phone_number="09102098929")
        self.order = baker.make(
            Order,
            customer=self.customer,
            total_price=Decimal(10.00),
            final_price=Decimal(10.00),
        )
        self.view = VerifyOrderView.as_view()
        self.url = reverse("verify_order")

    def test_Verify_GET(self):
        request = self.factory.get(self.url)
        request.user = self.customer
        request.session = {}
        request.session["order_pay"] = {
            "order_id": self.order.id,
        }
        request.GET = request.GET.copy()
        request.GET["Authority"] = "abcdefg123"
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
