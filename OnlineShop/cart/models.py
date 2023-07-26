from django.db import models
from core.models import BaseModel
from accounts.models import Customer
from products.models import Product
from core.utils import get_phonenumber_regex


class Cart(BaseModel):
   
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="cart")
    class Meta:
        verbose_name_plural = "carts"

    def __str__(self):
        return f"customer: {customer.fullname}"


class CartItem(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="cartItems",
        null=True,
        blank=True,
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cartItems",
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=2, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.cart}, {self.product}"
