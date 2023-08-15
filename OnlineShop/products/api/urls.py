from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register("categories", views.CategoryViewSet)
router.register("discounts", views.DiscountViewSet)

urlpatterns = [
    path("", views.ProductListCreateView.as_view(), name="products_api"),
    path("", include((router.urls))),
    path("<slug:slug>/",views.ProductDetailApiView.as_view(),name="product_detail_api",),
]
