from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import ProductDetailView, ProductListView
from products.api.views import (
    ProductDetailApiView,
    ProductListCreateView,
)


class TestUrls(SimpleTestCase):
    def test_products(self):
        url = reverse("products")
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_product_detail(self):
        url = reverse("product_detail", args=("girl-doll",))
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

    def test_products_api(self):
        url = reverse("products_api")
        self.assertEqual(resolve(url).func.view_class, ProductListCreateView)

    def test_product_detail_api(self):
        url = reverse("product_detail_api", args=("girl-doll",))
        self.assertEqual(resolve(url).func.view_class, ProductDetailApiView)
