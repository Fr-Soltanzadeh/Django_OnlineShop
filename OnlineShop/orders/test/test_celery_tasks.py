# import unittest
# from orders.tasks import send_order_status_email
# from unittest import TestCase, mock
# from django.conf import settings
# from django_celery_results.models import TaskResult

# class SendOrderStatusEmailTestCase(TestCase):
#     @mock.patch('orders.tasks.send_order_status_email')
#     def test_send_order_status_email_success(self, mock_send_mail):
#         # Mock the send_mail function to avoid actual email sending
#         mock_send_mail.return_value = 'result'

#         # Call the Celery task
#         result = send_order_status_email.delay('test@example.com', 'Test message', 'Test subject')
#         print(result)
#         mock_send_mail.assert_called_with('test@example.com', 'Test message', 'Test subject')

#         self.assertTrue(mock_send_mail.called)
#         self.assertTrue(mock_send_mail.send_order_status_email.called)        
# from celery.contrib.testing.worker import start_worker
# from django.core import mail
# from django.test import TestCase
# from orders.tasks import send_order_status_email

# class SendOrderStatusEmailTestCase(TestCase):
#     def setUp(self):
#         self.worker = start_worker(send_order_status_email)

#     def tearDown(self):
#         self.worker.terminate()

    # def test_send_order_status_email(self):
    #     # Set up test data
    #     target_mail = 'test@example.com'
    #     message = 'Test email message'
    #     mail_subject = 'Test email subject'

    #     # Call the task
    #     result = send_order_status_email.delay(target_mail, message, mail_subject)
    #     result.get()  # Wait for the task to complete

    #     # Verify the email was sent
    #     self.assertEqual(len(mail.outbox), 1)
    #     sent_email = mail.outbox[0]
    #     self.assertEqual(sent_email.subject, mail_subject)
    #     self.assertEqual(sent_email.body, message)
    #     self.assertEqual(sent_email.from_email, settings.EMAIL_HOST_USER)
    #     self.assertEqual(sent_email.to, [target_mail])