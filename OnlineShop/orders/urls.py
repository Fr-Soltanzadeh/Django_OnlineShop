from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import api_views, views

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("pay/<int:order_id>/", views.OrderPayView.as_view(), name="pay"),
    path("verify_order/", views.VerifyOrderView.as_view(), name="verufy_order"),
    path("order/api/v1/", api_views.OrderApiView.as_view(), name="order_api"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
