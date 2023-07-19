from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..forms import LoginForm, VerifyCodeForm
from ..views import LoginOrRegisterView, LogoutView
from ..models import User, OtpCode
from django.contrib.auth import authenticate


class TestLoginOrRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_GET(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'], LoginForm)
        
    def test_login_POST_valid(self):
        response = self.client.post(reverse('login'),
                                    data={'phone_number': '09102098929'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('verify_code'))
        self.assertEqual(OtpCode.objects.count(), 1)

    def test_login_POST_invalid(self):
        response = self.client.post(reverse('login'),
                                    data={'phone_number': '0910'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(form=response.context['form'], field='phone_number', errors=['invalid phone number'])


class TestVerifyCodeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post(reverse('login'),data={'phone_number': '09102098929'})
        self.otp_code= OtpCode.objects.get(phone_number="09102098929").code

    def test_VerifyCode_GET(self):
        response = self.client.get(reverse('verify_code'))
        self.assertTemplateUsed(response, 'accounts/verify_code.html')
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'], VerifyCodeForm)
        
    def test_VerifyCode_POST_valid(self):
        response = self.client.post(reverse('verify_code'),
                                    data={'verify_code': self.otp_code})
        self.user = User.objects.get(phone_number="09102098929")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(OtpCode.objects.count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile', args=(self.user.id,)))

    def test_VerifyCode_POST_invalid(self):
        response = self.client.post(reverse('verify_code'),
                                    data={'verify_code': "123"})
        self.assertEqual(OtpCode.objects.count(), 1)
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

        
class TestProfileView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(phone_number="09102098929", password="123")

    def test_profile_GET(self):
        response = self.client.get(reverse('profile', args=(self.user.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
