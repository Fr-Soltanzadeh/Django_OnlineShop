from django.test import TestCase
from ..forms import LoginForm
from ..models import User


class TestLoginForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(phone_number="09102098929", password="123")

    def test_valid_data(self):
        form = LoginForm(data={'phone_number': '09102098929', 'password': '123'})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors) , 2)

    def test_invalid_phonenumber(self):
        form = LoginForm(data={'phone_number': '0910', 'password': '123'})
        self.assertEqual(len(form.errors),1)
        self.assertTrue(form.has_error)
