from django.dispatch import Signal
from django.dispatch import receiver
from .models import Order
from django.db.models.signals import post_save
from .tasks import send_order_status_email


@receiver(post_save , sender=Order)
def handle_order_status_change(sender, instance, **kwargs):
    order = instance
    subject = "order status Update"
    message = f"Your order status wit RefId of {order.transaction_id} has been updated to {order.get_status_display()}"
    send_order_status_email.delay(order.customer.email, message, subject)
