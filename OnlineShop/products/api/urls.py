from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("", api_views.ProductListApiView.as_view(), name="products_api"),
    path("category/<slug:slug>",api_views.ProductListByCategoryApiView.as_view(),name="products_by_category_api",),
    path("<slug:slug>/",api_views.ProductDetailApiView.as_view(),name="product_detail_api",),
     path("categories/", views.CategoryApiView.as_view(), name="category_api"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
