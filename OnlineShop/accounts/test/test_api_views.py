from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..models import User, OtpCode
from rest_framework import status


class TestLoginOrRegisterApiView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url= reverse("login_api")

    def test_login_POST_valid(self):
        response = self.client.post(
            self.url, data={"phone_number": "09102098929"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OtpCode.objects.count(), 1)

    def test_login_POST_invalid(self):
        response = self.client.post(self.url, data={"phone_number": "0910"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class TestVerifyCodeApiView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url= reverse("verify_code_api")
        self.user = User.objects.create_user(phone_number="09102098929", password="123")
        self.client.post(reverse("login_api"), data={"phone_number": "09102098929"})
        self.client.session.save()
        self.otp_code = OtpCode.objects.get(phone_number="09102098929").code
   
    def test_VerifyCode_POST_valid(self):
        response = self.client.post(
            self.url, data={"verify_code": self.otp_code}
        )
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.user = User.objects.get(phone_number="09102098929")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(OtpCode.objects.count(), 0)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)

    def test_VerifyCode_POST_invalid(self):
        response = self.client.post(self.url, data={"verify_code": "123"})
        self.assertEqual(OtpCode.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestRefreshTokenApiView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url= reverse("refresh_token_api")

    def test_get_new_access_token_GET_invalid(self):
        response = self.client.get(self.url,headers={"Authorization":"123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
