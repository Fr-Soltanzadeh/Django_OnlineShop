from rest_framework import serializers
from cart.models import Cart, CartItem
from products.api.serializers import ProductSerializer
from accounts.api.serializers import CustomerSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ("product", "quantity")


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = (
            "customer",
            "cart_items",
            "total_price_with_discount",
            "final_price_without_shipping",
            "total_price",
        )
