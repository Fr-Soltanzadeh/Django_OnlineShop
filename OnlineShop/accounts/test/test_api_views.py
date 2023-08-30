from django.test import TestCase, RequestFactory, Client
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from ..models import User, OtpCode, Address, CustomerProfile
from accounts.api.serializers import (
    AddressSerializer,
    CustomerSerializer,
    CustomerAbstractSerializer,
    CustomerProfileSerializer,
)
from model_bakery import baker
from rest_framework import status


class TestLoginOrRegisterApiView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("login_api")

    def test_login_POST_valid(self):
        response = self.client.post(self.url, data={"phone_number": "09102098929"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OtpCode.objects.count(), 1)

    def test_login_POST_invalid(self):
        response = self.client.post(self.url, data={"phone_number": "0910"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestVerifyCodeApiView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("verify_code_api")
        self.user = User.objects.create_user(phone_number="09102098929", password="123")
        self.client.post(reverse("login_api"), data={"phone_number": "09102098929"})
        self.client.session.save()
        self.otp_code = OtpCode.objects.get(phone_number="09102098929").code

    def test_VerifyCode_POST_valid(self):
        response = self.client.post(self.url, data={"verify_code": self.otp_code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user = User.objects.get(phone_number="09102098929")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(OtpCode.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_VerifyCode_POST_invalid(self):
        response = self.client.post(self.url, data={"verify_code": "123"})
        self.assertEqual(OtpCode.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestRefreshTokenApiView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("refresh_token_api")

    def test_get_new_access_token_GET_invalid(self):
        response = self.client.get(self.url, headers={"Authorization": "123"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAddressesAPIView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(phone_number="09102098929")
        self.url = reverse("user_addresses_api")
        self.address = baker.make("Address", user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_addresses(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = AddressSerializer(Address.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_post_address(self):
        data = {
            "province": "Tehran",
            "city": "Tehran",
            "street": "p",
            "postal_code": 123,
            "detail": "d",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestAddressDetailAPIView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(phone_number="09102098929")
        self.address = baker.make("Address", user=self.user)
        self.url = reverse("user_address_api", args=(self.address.id,))
        self.client.force_authenticate(user=self.user)

    def test_get_address(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = AddressSerializer(Address.objects.get(id=self.address.id)).data
        self.assertEqual(response.data, expected_data)

    def test_put_address(self):
        data = {
            "user": self.user.id,
            "province": "Tehran",
            "city": "Tehran",
            "street": "p",
            "postal_code": 123,
            "detail": "d",
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_address_unauth_user(self):
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_address(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestCustomerAPIView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(phone_number="09102098929")
        self.url = reverse("customer_api")
        self.client.force_authenticate(user=self.user)

    def test_get_customer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CustomerSerializer(self.user).data
        self.assertEqual(response.data, expected_data)


class TestCustomerAbstractAPIView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(phone_number="09102098929")
        self.url = reverse("customeer_abstract_api")
        self.client.force_authenticate(user=self.user)

    def test_get_customer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CustomerAbstractSerializer(self.user).data
        self.assertEqual(response.data, expected_data)


class TestCustomerProfileAPIView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(phone_number="09102098929")
        self.profile = CustomerProfile.objects.create(customer=self.user)
        self.url = reverse("profile_api")
        self.client.force_authenticate(user=self.user)

    def test_get_customer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = CustomerProfileSerializer(self.profile).data
        self.assertEqual(response.data, expected_data)
