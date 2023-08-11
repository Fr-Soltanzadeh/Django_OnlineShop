from rest_framework import serializers
from cart.models import Cart, CartItem
from products.api.serializers import ProductSerializer
from accounts.api.serializers import CustomerSerializer
from datetime import datetime
from decimal import Decimal
import pytz


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ("product", "quantity")
        # depth=3


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_price_with_discount = serializers.SerializerMethodField()
    total_price_with_discount_coupon = serializers.SerializerMethodField()
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = (
            "customer",
            "cart_items",
            "total_price_with_discount",
            "total_price_with_discount_coupon",
            "total_price",
        )
        # depth=2

    def get_total_price_with_discount(self, cart):
        return cart.calculate_total_discounted_price()

    def get_total_price_with_discount_coupon(self, cart):
        return cart.calculate_final_price_without_shipping()

    def get_total_price(self, cart):
        return cart.calculate_total_price()
