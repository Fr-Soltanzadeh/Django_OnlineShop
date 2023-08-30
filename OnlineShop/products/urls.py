from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="products"),
    path("offer/", views.OfferedProductListView.as_view(), name="offer"),
    path("wishlist/", views.WishListProductView.as_view(), name="wishlist"),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]
