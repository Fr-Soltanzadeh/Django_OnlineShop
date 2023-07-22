from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('products/<slug:slug>', views.ProductListApiView.as_view(), name="products"),
    path('product/<slug:slug>', views.ProductDetailApiView.as_view(), name="product_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)