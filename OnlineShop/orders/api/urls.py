from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("", views.OrderApiView.as_view(), name="order_api"),
    path("<int:id>/", views.OrderDetailApiView.as_view(), name="order_detail_api"),
    path("apply_coupon/", views.ApplyCoupon.as_view(), name="apply_coupon_api"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
