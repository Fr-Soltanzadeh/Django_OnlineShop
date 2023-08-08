from rest_framework import serializers
from .models import Order, OrderItem
from accounts.serializers import CustomerSerializer


class OrderItemSerilizer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ("price", "quantity", "product")

    def get_product(self, order_item):
        return order_item.product.title


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerilizer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            "customer",
            "orderItems",
            "province",
            "city",
            "street",
            "address_detail",
            "postal_code",
            "total_price",
            "final_price",
            "receiver_fullname",
            "receiver_phone_number",
            "shipping",
        )