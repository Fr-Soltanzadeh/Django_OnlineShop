from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..views import ProductDetailView, ProductListView


class TestProductDetailView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ProductDetail_GET(self):
        response = self.client.get(reverse("product_detail", args=("girl-doll",)))
        self.assertTemplateUsed(response, "products/product_details.html")
        self.assertEqual(response.status_code, 200)


class TestProductListView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ProductList_GET(self):
        response = self.client.get(reverse("products"))
        self.assertTemplateUsed(response, "products/product_list.html")
        self.assertEqual(response.status_code, 200)
