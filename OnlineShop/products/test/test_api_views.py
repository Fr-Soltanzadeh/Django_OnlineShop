from django.test import TestCase, RequestFactory
from django.urls import reverse
from products.api.views import (
    ProductDetailApiView,
    ProductListCreateView,
)
from ..models import Category, Product, Comment, Discount
from rest_framework import status
from products.api.serializers import ProductSerializer, CategorySerializer, CommentSerializer, DiscountSerializer
from decimal import Decimal
from model_bakery import baker
from rest_framework.test import APIClient, APITestCase
from accounts.models import User


class TestProductDetailView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            phone_number="09102098929",
            password="123",
            email="admin@example.com"
        )
        category = Category.objects.create(name="dolls")
        self.product = Product.objects.create(
            category=category,
            title="girl_doll",
            slug="girl-doll",
            price=Decimal(20.00),
            quantity=10,
            info="a"
        )

    def test_ProductDetail_GET(self):
        response = self.client.get(
            reverse("product_detail_api", args=(self.product.slug,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.product.title)

    def test_ProductDetail_UPDATE(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("product_detail_api", args=(self.product.slug,))
        data = {"title": "doll", "price": self.product.price, "slug":self.product.slug, "info":self.product.info}
        response = self.client.put(
            url, data, partial=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])


    def test_ProductDetail_DELETE(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("product_detail_api", args=(self.product.slug,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(slug=self.product.slug).exists())

    

class ProductListCreateView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category1 = Category.objects.create(name="dolls", slug="dolls")
        self.category2 = Category.objects.create(name="books", slug="books")
        self.product1 = baker.make(
            Product,
            title="Product 1",
            info="",
            category=self.category1,
            price=Decimal(10.00),
            discount=None,
            slug="product-1",
        )
        self.product2 = baker.make(
            Product,
            title="Product 2",
            info="",
            category=self.category2,
            price=Decimal(10.00),
            discount=None,
            slug="product-2",
        )

    def test_ProductList_GET(self):
        response = self.client.get(reverse("products_api"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(len(response.data["results"]), len(serializer.data))
        self.assertEqual(response.data["results"][0]["title"], serializer.data[0]["title"])


class CategoryApiViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/v1/products/categories/"
        Category.objects.create(name="Category 1", slug="Category1")
        Category.objects.create(name="Category 2", slug="Category2")
        Category.objects.create(name="Category 3", slug="Category3")

    def test_get_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CategorySerializer(Category.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

class CommentApiViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        category = Category.objects.create(name="dolls")
        self.product = Product.objects.create(
            category=category,
            title="girl_doll",
            slug="girl-doll",
            price=Decimal(20.00),
            quantity=10,
            info="a",
            id=1
        )
        self.url = "/api/v1/products/comments/?product_pk=1"
        comment1= baker.make(Comment, product=self.product)
        comment2= baker.make(Comment, product=self.product)

    def test_get_comments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CommentSerializer(Comment.objects.filter(product=self.product), many=True).data
        self.assertEqual(response.data, expected_data)


class DiscountApiViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            phone_number="09102098929",
            password="123",
            email="admin@example.com"
        )        
        self.url = "/api/v1/products/discounts/"
        discount1= baker.make(Discount)
        self.client.force_authenticate(user=self.admin_user)


    def test_get_discounts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = DiscountSerializer(Discount.objects.all(), many=True).data
        self.assertEqual(response.data['results'], expected_data)