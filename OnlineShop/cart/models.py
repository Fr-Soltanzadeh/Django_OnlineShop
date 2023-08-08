from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Product
from core.utils import get_phonenumber_regex
from orders.models import Coupon


class Cart(BaseModel):

    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    coupon = models.OneToOneField(
        Coupon, on_delete=models.SET_NULL, related_name="cart", null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "carts"

    def __str__(self):
        return f"customer{self.customer.id} {self.customer.fullname}"

    def calculate_final_price_without_shipping(self):
        if self.coupon:
            return (
                sum(
                    (
                        item.product.discounted_price * item.quantity
                        for item in self.cart_items.all()
                    )
                )
                * (100 - self.coupon.percent)
                / 100
            )
        return sum(
            (
                item.product.discounted_price * item.quantity
                for item in self.cart_items.all()
            )
        )

    def calculate_total_price(self):
        return sum(
            (item.product.price * item.quantity for item in self.cart_items.all())
        )


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
        unique_together = ["cart", "product"]
