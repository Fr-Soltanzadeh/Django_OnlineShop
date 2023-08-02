from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerProfile, Customer
from cart.models import Cart


@receiver(post_save, sender=Customer)
def create_customer_profile(sender, instance=None, created=False, **kwargs):
    if created:
        CustomerProfile.objects.create(customer=instance)


@receiver(post_save, sender=Customer)
def create_cart(sender, instance=None, created=False, **kwargs):
    if created:
        Cart.objects.create(customer=instance)
