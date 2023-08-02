from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from products.models import Category
from products.serializers import CategorySerializer


class HomeApiViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("home_api")
        Category.objects.create(name="Category 1", slug="Category1")
        Category.objects.create(name="Category 2", slug="Category2")
        Category.objects.create(name="Category 3", slug="Category3")

    def test_get_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CategorySerializer(Category.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)
