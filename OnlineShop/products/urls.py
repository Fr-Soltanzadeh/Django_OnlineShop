from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/<slug:slug>/",views.ProductListByCategoryView.as_view(),name="products_by_category",),
    path("product/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]
