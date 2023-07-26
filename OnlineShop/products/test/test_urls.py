from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import ProductDetailView, ProductListByCategoryView, ProductListView


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

   