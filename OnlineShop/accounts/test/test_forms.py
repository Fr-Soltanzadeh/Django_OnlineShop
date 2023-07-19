from django.test import TestCase
from ..forms import LoginForm, VerifyCodeForm
from ..models import User


class TestLoginForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(phone_number="09102098929", password="123")

    def test_valid_data(self):
        form = LoginForm(data={'phone_number': '09102098929'})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())

    def test_invalid_phonenumber(self):
        form = LoginForm(data={'phone_number': '0910'})
        self.assertTrue(form.has_error)


class TestVerifyCodeForm(TestCase):

    def test_empty_data(self):
        form = VerifyCodeForm(data={})
        self.assertFalse(form.is_valid())

    def test_valid_data(self):
        form = VerifyCodeForm(data={'verify_code': '1234'})
        self.assertTrue(form.is_valid())