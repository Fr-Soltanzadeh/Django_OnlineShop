from django.test import TestCase
from ..models import User


class TestUserModel(TestCase):

    def setUp(self) :
        self.user = User.objects.create(phone_number='09102098929', password='123', first_name="Farzaneh", last_name="Soltanzadeh")

    def test_model_str(self):
        self.assertEqual(str(self.user), '09102098929')

    def test_model_fullname(self):
        self.assertEqual(self.user.fullname, 'Farzaneh Soltanzadeh')
