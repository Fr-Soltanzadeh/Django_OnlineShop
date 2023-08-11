from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="products"),
    path("category/<slug:slug>/",views.ProductListByCategoryView.as_view(),name="products_by_category",),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]
