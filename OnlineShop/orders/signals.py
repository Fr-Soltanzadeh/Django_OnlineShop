from django.dispatch import Signal
from django.dispatch import receiver
from .models import Order
from django.db.models.signals import post_save
from .tasks import send_order_status_email


@receiver(post_save , sender=Order)
def handle_order_status_change(sender, instance, created=None, **kwargs):
    
    order = instance
    if created:
        subject = "New Order"
        message = f"Your order has been successfully placed. Status:{order.get_status_display()}"
    elif order.status==3:
        subject = "Order Pay Failed"
        message = f"Transaction failed, please try again."
    else:
        subject = "Order Status Update"
        message = f"Your order status with RefId of {order.transaction_id} has been updated to {order.get_status_display()}"
    
    send_order_status_email.delay(order.customer.email, message, subject)
