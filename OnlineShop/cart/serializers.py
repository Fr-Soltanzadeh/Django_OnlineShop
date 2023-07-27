from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ("product","quantity")
        # depth=3


class CartSerializer(serializers.ModelSerializer):
    cartItems=CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ("customer","cartItems")
        # depth=2


