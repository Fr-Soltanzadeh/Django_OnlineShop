from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import api_views, views

urlpatterns = [
    path('cart/api/', api_views.CartApiView.as_view(), name="cart_api"),
    path('cart/api/add/', api_views.AddToCartApiView.as_view(), name="add_to_cart_api"),
    path('cart/', views.CartView.as_view(), name="cart"),
]

urlpatterns = format_suffix_patterns(urlpatterns)