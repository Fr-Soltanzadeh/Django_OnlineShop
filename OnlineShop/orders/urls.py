from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import api_views, views

urlpatterns = [
    # path("checkout/api/v1/", api_views.CheckoutApiView.as_view(), name="checkout_api"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
