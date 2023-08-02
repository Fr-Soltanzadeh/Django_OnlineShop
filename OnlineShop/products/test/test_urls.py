from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import ProductDetailView, ProductListByCategoryView, ProductListView
from ..api_views import (
    ProductDetailApiView,
    ProductListApiView,
    ProductListByCategoryApiView,
)


class TestUrls(SimpleTestCase):
    def test_products(self):
        url = reverse("products")
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_products_by_category(self):
        url = reverse("products_by_category", args=("dolls",))
        self.assertEqual(resolve(url).func.view_class, ProductListByCategoryView)

    def test_product_detail(self):
        url = reverse("product_detail", args=("girl-doll",))
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

    def test_products_api(self):
        url = reverse("products_api")
        self.assertEqual(resolve(url).func.view_class, ProductListApiView)

    def test_products_by_category_api(self):
        url = reverse("products_by_category_api", args=("dolls",))
        self.assertEqual(resolve(url).func.view_class, ProductListByCategoryApiView)

    def test_product_detail_api(self):
        url = reverse("product_detail_api", args=("girl-doll",))
        self.assertEqual(resolve(url).func.view_class, ProductDetailApiView)
