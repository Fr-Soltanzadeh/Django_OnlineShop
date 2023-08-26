from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Product
from core.utils import get_phonenumber_regex
from orders.models import Coupon
import pytz
from datetime import datetime
from django.db.models import Sum, F


class Cart(BaseModel):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    coupon = models.OneToOneField(
        Coupon, on_delete=models.SET_NULL, related_name="cart", null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "carts"

    def __str__(self):
        return f"customer{self.customer.id} {self.customer.fullname}"
    
    @property
    def final_price_without_shipping(self):
        cart_items = self.cart_items.select_related("product")
        total_price = sum(
            item.product.discounted_price * item.quantity for item in cart_items
        )
        if (
            self.coupon
            and self.coupon.is_active
            and self.coupon.end_time > datetime.now().replace(tzinfo=pytz.utc)
        ):
            return total_price * (1 - self.coupon.percent / 100)
        return total_price
    
    @property
    def total_price_with_discount(self):
        cart_items = self.cart_items.select_related("product")
        return sum(item.product.discounted_price * item.quantity for item in cart_items)
    
    @property
    def total_price(self):
        cart_items = self.cart_items.select_related("product")
        return cart_items.aggregate(
            total_price=Sum(F("product__price") * F("quantity"))
        )["total_price"]


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
