from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from .models import Order
import requests
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.tasks import send_order_status_email


class CheckoutView(View):
    template_name = "orders/checkout.html"

    def get(self, request):
        return render(request, self.template_name)


if settings.SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "www"

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = (
    f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
)
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = "http://127.0.0.1:8000/orders/verify_order/"


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session["order_pay"] = {
            "order_id": order.id,
        }
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": int(round(float(order.total_price))) * 1000,
            "Description": description,
            "CallbackURL": CallbackURL,
            "metadata": {"mobile": order.customer.phone_number},
        }
        data = json.dumps(data)
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "content-length": str(len(data)),
        }
        try:
            response = requests.post(
                ZP_API_REQUEST, data=data, headers=headers, timeout=10
            )
            if response.status_code == 200:
                response = response.json()
                if response["Status"] == 100:
                    return redirect(ZP_API_STARTPAY + str(response["Authority"]))
                elif response.get("errors"):
                    e_code = response["errors"]["code"]
                    e_message = response["errors"]["message"]
                    return HttpResponse(
                        f"Error code: {e_code}, Error Message: {e_message}"
                    )
            return HttpResponse(response.items())

        except requests.exceptions.Timeout:
            return {"status": False, "code": "timeout"}
        except requests.exceptions.ConnectionError:
            return {"status": False, "code": "connection error"}


class VerifyOrderView(View):
    def get(self, request):
        order_id = request.session["order_pay"]["order_id"]
        order = Order.objects.select_related("customer").get(id=int(order_id))
        cart = order.customer.cart
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": int(round(float(order.total_price))) * 1000,
            "Authority": request.GET["Authority"],
        }
        data = json.dumps(data)
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "content-length": str(len(data)),
        }

        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        

        if response.status_code == 200 and response.json()["Status"] in [100,101]:
            order.status = 2
            response=response.json()
            order.transaction_id = response["RefID"]
            order.save()
            
            if cart.coupon:
                coupon = cart.coupon
                coupon.is_active = False
                coupon.save()
                cart.coupon = None
                cart.save()

            for item in cart.cart_items.all():
                item.delete()

            if order.customer.email:
                mail = order.customer.email
                message = f"Transaction success.RefID:  {str(response['RefID'])}"
                mail_subject = "Order Confirmed Successfuly"
                send_order_status_email.delay(mail, message, mail_subject)

            return HttpResponse(
                f"Transaction success.RefID:  {str(response['RefID'])}, Status: {response['Status']}, order ID: {order_id}"
            )
        else:
            order.status = 3
            order.save()
            for item in cart.cart_items.select_related("product"):
                product = item.product
                product.quantity += item.quantity
                if not product.is_active:
                    product.is_active = True
                product.save()
            return HttpResponse("Transaction failed, order ID:" + str(order_id))
