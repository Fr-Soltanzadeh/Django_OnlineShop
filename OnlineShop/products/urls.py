from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import api_views, views

urlpatterns = [
    path('products/api/', api_views.ProductListApiView.as_view(), name="products_api"),
    path('products/api/<slug:slug>/', api_views.ProductListByCategoryApiView.as_view(), name="products_by_category_api"),
    path('product/api/<slug:slug>/', api_views.ProductDetailApiView.as_view(), name="product_detail_api"),
    path('products/', views.ProductListView.as_view(), name="products"),
    path('products/<slug:slug>/', views.ProductListByCategoryView.as_view(), name="products_by_category"),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name="product_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)