from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('products/<slug:slug>', views.ProductListApiView.as_view()),
    path('product/<slug:slug>', views.ProductDetailApiView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)