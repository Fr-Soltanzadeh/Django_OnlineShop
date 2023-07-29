from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import CustomerProfile, Customer
from cart.models import Cart


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Customer)
def create_customer_profile(sender, instance=None, created=False, **kwargs):
    if created:
        CustomerProfile.objects.create(customer=instance)


@receiver(post_save, sender=User)
def create_cart(sender, instance=None, created=False, **kwargs):
    if created and instance.role==1:
        Cart.objects.create(customer=instance)