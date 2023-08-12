from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import reverse
from rest_framework import views, permissions, status
from .serializers import OrderSerializer
from ..models import Order, OrderItem, Coupon
from accounts.models import Address
from django.http import HttpResponseRedirect
from datetime import datetime
import pytz


class OrderApiView(APIView):
    def post(self, request):
        user = request.user
        cart = user.cart
        data = request.data
        address = Address.objects.get(id=int(data["address_id"]))
        order_data = {
            "customer": user,
            "province": address.province,
            "postal_code": address.postal_code,
            "city": address.city,
            "address_detail": address.detail,
            "street": address.street,
            "total_price": cart.calculate_total_price(),
            "receiver_fullname": data["receiver_fullname"],
            "receiver_phone_number": data["receiver_phone_number"],
            "coupon": cart.coupon,
        }
        order = Order.objects.create(
            customer=user,
            province=address.province,
            postal_code=address.postal_code,
            city=address.city,
            address_detail=address.detail,
            street=address.street,
            total_price=cart.calculate_total_price(),
            receiver_fullname=data["receiver_fullname"],
            receiver_phone_number=data["receiver_phone_number"],
            coupon=cart.coupon,
        )

        for item in cart.cart_items.all():
            OrderItem.objects.create(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                order=order,
            )
        order.calculate_final_price()
        order.save()
        return HttpResponseRedirect(redirect_to=reverse("pay", args=(order.id,)))


class ApplyCoupon(APIView):
    def post(self, request):
        coupon_code = request.data.get("coupon_code")
        if Coupon.objects.filter(coupon_code=coupon_code).exists():
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            if coupon.is_active and coupon.end_time > datetime.now().replace(
                tzinfo=pytz.utc
            ):
                cart = request.user.cart
                cart.coupon = coupon
                cart.save()
                return Response(data={"is_valid": True})
        return Response(data={"is_valid": False})