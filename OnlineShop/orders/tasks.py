from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(bind=True)
def send_notification_mail(self, target_mail, message, mail_subject):
    logger.info("Your message here")
    print("*******************************************************")
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[target_mail],
        fail_silently=False,
        )
    print("done")
    return "Done"
