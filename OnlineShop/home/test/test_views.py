from django.test import TestCase, Client
from django.urls import reverse
from ..views import HomeView


class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_Home_GET(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home/index.html")
        self.assertEqual(response.status_code, 200)
