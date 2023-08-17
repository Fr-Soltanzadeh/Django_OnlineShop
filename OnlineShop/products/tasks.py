from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import Customer

@shared_task(bind=True)
def send_ad_mails(self):
    mail_subject = "Long time no see!"
    message = "Hi. Visit our site for wonderful new products for your sweet child.\n "
    recipient_list = [customer.email for customer in Customer.objects.all() if customer.email]
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    return "Done"
