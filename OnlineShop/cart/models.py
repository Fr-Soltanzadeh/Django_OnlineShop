from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Product
from core.utils import get_phonenumber_regex


class Cart(BaseModel):
   
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    class Meta:
        verbose_name_plural = "carts"

    def __str__(self):
        return f"customer{self.customer.id} {self.customer.fullname}"


class CartItem(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="cart_items",
        null=True,
        blank=True,
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart}, {self.product}"

    class Meta:
        verbose_name_plural = "cart items"
        unique_together = ['cart', 'product']