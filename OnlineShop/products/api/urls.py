from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register("categories", views.CategoryViewSet)
router.register("discounts", views.DiscountViewSet)

urlpatterns = [
    path("", include((router.urls))),
    path("", views.ProductListApiView.as_view(), name="products_api"),
    path(
        "category/<slug:slug>/",
        views.ProductListByCategoryApiView.as_view(),
        name="products_by_category_api",
    ),
    path(
        "<slug:slug>/",
        views.ProductDetailApiView.as_view(),
        name="product_detail_api",
    ),
]
