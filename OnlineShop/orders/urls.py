from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import api_views, views

urlpatterns = [
    # path("checkout/api/v1/", api_views.CheckoutApiView.as_view(), name="checkout_api"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("pay/<int:order_id>/", views.OrderPayView.as_view(), name="pay"),
    path("verify_order/", views.VerifyOrderView.as_view(), name="verufy_order"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
