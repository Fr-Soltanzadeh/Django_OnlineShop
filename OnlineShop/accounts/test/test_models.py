from django.test import TestCase
from ..models import User, OtpCode, Address, CustomerProfile, Customer
from model_bakery import baker
from django.urls import reverse


class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            phone_number="09102098929",
            password="123",
            first_name="Farzaneh",
            last_name="Soltanzadeh",
        )

    def test_model_str(self):
        self.assertEqual(str(self.user), "09102098929")

    def test_model_fullname(self):
        self.assertEqual(self.user.fullname, "Farzaneh Soltanzadeh")


class TestCustomerProfileModel(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(phone_number="09102098929")
        self.profile = CustomerProfile.objects.get(customer=self.customer)

    def test_model_str(self):
        self.assertEqual(str(self.profile), "09102098929")


# class TestAddressModel(TestCase):

#     def setUp(self) :
#         self.user = User.objects.create(phone_number='09102098929', password='123')
#         self.address = baker.make(Address, user=self.user, country="Iran", province="Tehran", city="Tehran", street="Piroozi")
#         # self.address = Address.objects.create(country="Iran", province="Tehran", city="Tehran", street="Piroozi", detail="a", postal_code=1)

#     def test_model_str(self):
#         print(str(self.address))
#         self.assertEqual(str(self.address), 'Piroozi, Tehran, Tehran, Iran')


class TestOtpCodeModel(TestCase):
    def setUp(self):
        self.otpCode = baker.make(
            OtpCode,
            phone_number="09102098929",
            code="123",
        )

    def test_model_str(self):
        self.assertEqual(str(self.otpCode), "09102098929 - 123")
