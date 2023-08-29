from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import reverse
from rest_framework import views, permissions, status
from .serializers import OrderSerializer, CouponSerializer
from ..models import Order, OrderItem, Coupon
from accounts.models import Address
from accounts.permissions import IsAdminUserOrReadOnly
from django.http import HttpResponseRedirect
from datetime import datetime
import pytz


class OrderApiView(APIView):
    def post(self, request):
        user = request.user
        cart = user.cart
        data = request.data
        address = Address.objects.get(id=int(data["address_id"]))
        cart_items = cart.cart_items.select_related("product")
        for item in cart_items:
            product = item.product
            if product.quantity == 0:
                return Response(
                    {
                        "message": f"Sorry, the item {product.title} in your cart is not available now."
                    }
                )
            elif product.quantity < item.quantity:
                return Response(
                    {
                        "message": f"There are only {product.quantity} number of {product.title} available now."
                    }
                )
        order = Order.objects.create(
            customer=user,
            province=address.province,
            postal_code=address.postal_code,
            city=address.city,
            address_detail=address.detail,
            street=address.street,
            total_price=cart.total_price,
            receiver_fullname=data["receiver_fullname"],
            receiver_phone_number=data["receiver_phone_number"],
            coupon=cart.coupon,
        )
        for item in cart_items:
            OrderItem.objects.create(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                order=order,
            )
        order.calculate_final_price()
        order.save()
        return HttpResponseRedirect(redirect_to=reverse("pay", args=(order.id,)))

    def get(self, request):
        user = request.user
        orders = (
            user.orders.prefetch_related("orderItems")
            .select_related("customer")
            .order_by("created_at")
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class ApplyCoupon(APIView):
    def post(self, request):
        coupon_code = request.data.get("coupon_code")
        serializer = CouponSerializer(data=coupon_code)
        if serializer.is_valid():
            if Coupon.objects.filter(
                coupon_code=serializer.data["coupon_code"]
            ).exists():
                coupon = Coupon.objects.get(coupon_code=coupon_code)
                if coupon.is_active and coupon.end_time > datetime.now().replace(
                    tzinfo=pytz.utc
                ):
                    cart = request.user.cart
                    cart.coupon = coupon
                    cart.save()
                    return Response(data={"is_valid": True})
        return Response(data={"is_valid": False})


class OrderDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Order.objects.prefetch_related("orderItems").select_related("customer")
    serializer_class = OrderSerializer
