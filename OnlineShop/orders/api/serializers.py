from rest_framework import serializers
from ..models import Order, OrderItem
from accounts.api.serializers import CustomerSerializer


class OrderItemSerilizer(serializers.ModelSerializer):
    product = serializers.CharField(source="product.title")
    class Meta:
        model = OrderItem
        fields = ("price", "quantity", "product")


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerilizer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    status = serializers.CharField(source="get_status_display")
    created_at = serializers.SerializerMethodField()

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
            "created_at",
            "status",
        )

    def get_created_at(self, order):
        return order.created_at.date()
