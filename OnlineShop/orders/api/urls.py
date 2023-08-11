from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("", api_views.OrderApiView.as_view(), name="order_api"),
    path(
        "apply_coupon/", api_views.ApplyCoupon.as_view(), name="apply_coupon_api"
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
