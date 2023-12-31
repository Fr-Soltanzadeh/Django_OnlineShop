from rest_framework import serializers
from ..models import Order, OrderItem
from accounts.api.serializers import CustomerSerializer
from core.utils import get_phonenumber_regex

class OrderItemSerilizer(serializers.ModelSerializer):
    product = serializers.CharField(source="product.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ("price", "quantity", "product")


class CouponSerializer(serializers.Serializer):
    coupon_code = serializers.IntegerField(min_value=1000, max_value=9999)


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerilizer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    status = serializers.CharField(source="get_status_display")
    created_at = serializers.SerializerMethodField(read_only=True)

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

class RecieverSerializer(serializers.Serializer):
    receiver_fullname= serializers.CharField()
    receiver_phone_number= serializers.CharField(validators=[get_phonenumber_regex()])