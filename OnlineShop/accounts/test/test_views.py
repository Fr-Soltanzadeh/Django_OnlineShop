from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..forms import LoginForm
from ..views import LoginView, LogoutView
from ..models import User
from django.contrib.auth import authenticate


class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(phone_number="09102098929", password="123")

    def test_login_GET(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'], LoginForm)

    def test_login_POST_valid(self):
        response = self.client.post(reverse('login'),
                                    data={'phone_number': '09102098929', 'password': '123'})
        self.assertEqual(response.status_code, 302)

    def test_login_POST_invalid_password(self):
        response = self.client.post(reverse('login'),
                                    data={'phone_number': '09102098929', 'password': '321'})
        self.assertEqual(response.status_code, 200)
    
    def test_login_POST_invalid_username(self):
        response = self.client.post(reverse('login'),
                                    data={'phone_number': '09105021591', 'password': '123'})
        self.assertEqual(response.status_code, 200)


class TestLogoutView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout_GET_authenticated_user(self):
        user = User.objects.create_user(phone_number="09102098929", password="123")
        self.client.login(phone_number="09102098929", password="123")
        response = self.client.get(reverse('logout'))
        # user = authenticate(username='john', password='password')
        # self.assertIsNone(user)        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_logout_GET_anonymous_user(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        
