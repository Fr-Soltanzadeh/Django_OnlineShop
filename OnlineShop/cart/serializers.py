from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer
from accounts.serializers import CustomerSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ("product", "quantity")
        # depth=3


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    grand_price = serializers.SerializerMethodField()
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ("customer", "cart_items", "grand_price", "total_price")
        # depth=2

    def get_grand_price(self, cart):
        return cart.calculate_final_price_without_shipping()

    def get_total_price(self, cart):
        return cart.calculate_total_price()
