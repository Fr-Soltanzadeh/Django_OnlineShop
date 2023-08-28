from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import Order, OrderItem, Coupon
from cart.models import Cart, CartItem
from accounts.models import Address, User
from products.models import Product
from model_bakery import baker
from decimal import Decimal
from rest_framework import status
from datetime import datetime, timedelta


class OrderApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(phone_number="09102098929")
        self.url = reverse("order_api")

        # Create a cart for the user
        self.cart = Cart.objects.create(customer=self.user)

        # Create an address for the user
        self.address = Address.objects.create(
            user=self.user,
            province="Test Province",
            postal_code=12345,
            city="Test City",
            detail="Test Address",
            street="Test Street",
        )

        # Add items to the cart
        self.product = baker.make(Product, info="", price=Decimal(10.00))
        self.cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product, quantity=2
        )

    def test_create_order_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "address_id": self.address.id,
            "receiver_fullname": "Farzaneh Soltanzadeh",
            "receiver_phone_number": "091020989290",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(customer=self.user)
        self.assertTrue(response.url.startswith(reverse("pay", args=(order.id,))))

        # Assert that the order has been created with the correct data

        self.assertEqual(order.province, self.address.province)
        self.assertEqual(order.postal_code, self.address.postal_code)
        self.assertEqual(order.city, self.address.city)
        self.assertEqual(order.address_detail, self.address.detail)
        self.assertEqual(order.street, self.address.street)
        self.assertEqual(order.total_price, self.cart.total_price)
        self.assertEqual(order.receiver_fullname, "Farzaneh Soltanzadeh")
        self.assertEqual(order.receiver_phone_number, "091020989290")

        # Assert that the order items have been created correctly
        order_items = OrderItem.objects.filter(order=order)
        self.assertEqual(order_items.count(), 1)
        self.assertEqual(order_items[0].product, self.cart_item.product)
        self.assertEqual(order_items[0].quantity, self.cart_item.quantity)
        self.assertEqual(order_items[0].price, self.cart_item.product.price)

    def test_create_order_unauthenticated_user(self):
        data = {
            "address_id": self.address.id,
            "receiver_fullname": "Farzaneh Soltanzadeh",
            "receiver_phone_number": "091020989290",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 401)


class ApplyCouponViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(phone_number="09102098929")
        self.url = reverse("apply_coupon_api")
        self.cart = Cart.objects.create(customer=self.user)
        self.coupon = baker.make(
            Coupon,
            coupon_code=1234,
            is_active=True,
            end_time=datetime.now() + timedelta(days=1),
        )

    def test_valid_coupon(self):
        self.client.force_authenticate(user=self.user)
        data = {"coupon_code": 1234}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"is_valid": True})
        self.assertEqual(self.cart.coupon, self.coupon)

    def test_invalid_coupon(self):
        self.client.force_authenticate(user=self.user)
        data = {"coupon_code": 5678}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"is_valid": False})
        self.assertIsNone(self.cart.coupon)

    def test_unauthenticated_user(self):
        data = {"coupon_code": 1234}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
