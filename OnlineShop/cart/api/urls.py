from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import  views

urlpatterns = [
    path("", views.CartApiView.as_view(), name="cart_api"),
    path(
        "add/", views.AddToCartApiView.as_view(), name="add_to_cart_api"
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
