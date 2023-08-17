from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Product, Category
from cart.api.serializers import CartSerializer
from products.api.serializers import ProductSerializer
from ..models import CartItem, Cart
from model_bakery import baker
from accounts.models import User
from decimal import Decimal


class TestAddToCartApiView(APITestCase):
    def setUp(self):
        self.category=baker.make(Category)
        self.product = baker.make(Product, info="", price=Decimal(10.00), category=self.category)
        self.url = reverse("add_to_cart_api")

    def test_add_to_cart_authenticated(self):
        self.user = User.objects.create(phone_number="09102098929", role=1)
        self.cart = Cart.objects.create(customer=self.user)
        self.client.force_authenticate(user=self.user)
        data = {"product_id": self.product.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertIn("cart_items", response.data)
        self.assertIn("total_price", response.data)

    def test_add_to_cart_unauthenticated_user(self):
        self.client.logout()
        response = self.client.post(self.url, data={"product_id": self.product.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = ProductSerializer(self.product).data
        product_data["price"] = str(product_data["price"])
        product_data["discounted_price"] = "10.00"
        expected_cart_data = {
            "customer": None,
            "cart_items": [{"quantity": 1, "product": product_data}],
            "total_price_with_discount": "10.00",
            "total_price": "10.00",
        }
        self.assertEqual(response.data, expected_cart_data)


class TestCartApiView(APITestCase):
    def setUp(self):
        self.category=baker.make(Category)
        self.product = baker.make(Product, info="", category=self.category)
        self.user = User.objects.create(phone_number="09102098929", role=1)
        self.cart = Cart.objects.create(customer=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2
        )
        self.url = reverse("cart_api")

    def test_get_cart_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CartSerializer(self.cart).data
        self.assertEqual(response.data, expected_data)

    def test_delete_cart_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_put_cart_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {"cart_items": [{"product_id": self.product.id, "quantity": 3}]}
        response = self.client.put(self.url, data=data, content_type="application/json")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_cart_unauthenticated(self):
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "customer": None,
            "cart_items": [],
            "total_price_with_discount": "0",
            "total_price": "0",
        }
        self.assertEqual(response.data, expected_data)

    def test_get_cart_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "customer": None,
            "cart_items": [],
            "total_price_with_discount": "0",
            "total_price": "0",
        }
        self.assertEqual(response.data, expected_data)
