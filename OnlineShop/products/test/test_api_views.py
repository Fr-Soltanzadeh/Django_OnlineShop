from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from products.api.views import (
    ProductDetailApiView,
    ProductListApiView,
    ProductListByCategoryApiView,
)
from ..models import Category, Product
from rest_framework import status
from products.api.serializers import ProductSerializer, CategorySerializer
from decimal import Decimal
from model_bakery import baker
from rest_framework.test import APIClient, APITestCase

class TestProductListByCategoryView(APITestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="dolls", slug="dolls")
        self.product1 = baker.make(
            Product, title="Product 1", info="", category=self.category
        )
        self.product2 = baker.make(
            Product, title="Product 2", info="", category=self.category
        )

    def test_ProductListByCategory_GET(self):
        response = self.client.get(reverse("products_by_category_api", args=("dolls",)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = Product.objects.filter(category=self.category)
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data["results"], serializer.data)


class TestProductDetailView(APITestCase):
    def setUp(self):
        self.client = Client()
        category = Category.objects.create(name="dolls")
        self.product = Product.objects.create(
            category=category,
            title="girl_doll",
            slug="girl-doll",
            price=30.00,
            quantity=10,
        )

    def test_ProductDetail_GET(self):
        response = self.client.get(
            reverse("product_detail_api", args=(self.product.slug,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.product.title)

    def test_ProductDetail_DELETE(self):
        url = reverse("product_detail_api", args=(self.product.slug,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(slug=self.product.slug).exists())

    def test_ProductDetail_UPDATE(self):
        url = reverse("product_detail_api", args=(self.product.slug,))
        data = {"title": "doll", "slug": "doll", "price": Decimal(20.00), "info": "a"}
        response = self.client.put(
            url, data, content_type="application/json", partial=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])


class TestProductListView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ProductList_GET(self):
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class CategoryApiViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("category_api")
        Category.objects.create(name="Category 1", slug="Category1")
        Category.objects.create(name="Category 2", slug="Category2")
        Category.objects.create(name="Category 3", slug="Category3")

    def test_get_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CategorySerializer(Category.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)
