from django.test import TestCase
from products.tasks import send_ad_mails
from unittest import mock
from accounts.models import Customer


class send_ad_mailsTestCase(TestCase):
    @mock.patch('products.tasks.send_mail')
    def test_send_ad_mails_success(self, mock_send_mail):
        customer=Customer.objects.create(phone_number='09102098929', email='test@gmail.com')
        # Mock the send_mail function to avoid actual email sending
        instance = mock_send_mail.return_value
        # Call the Celery task
        result = send_ad_mails.delay()
        print(result.get())
        self.assertEqual(result.get(), "Done")