from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Product
from core.utils import get_phonenumber_regex
from decimal import Decimal


class Coupon(BaseModel):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    coupon_code = models.IntegerField(unique=True)
    percent = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "coupons"

    def __str__(self):
        return f"{self.coupon_code} {self.title} {self.percent}%"


class Order(BaseModel):
    class StatusChoice(models.IntegerChoices):
        PENDING = 1, "PENDING"
        PAID = 2, "PAID"
        PAYMENT_FAILED = 3, "PAYMENT_FAILED"
        SENDING = 4, "SENDING"
        DELIVERED = 5, "DELIVERED"
        CANCEL = 6, "CANCEL"

    status = models.IntegerField(choices=StatusChoice.choices, default=1)
    customer = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="orders", null=True
    )
    province = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    address_detail = models.CharField(max_length=300, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    final_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    receiver_fullname = models.CharField(max_length=100, null=True, blank=True)
    receiver_phone_number = models.CharField(
        max_length=14, validators=[get_phonenumber_regex()], null=True, blank=True
    )
    transaction_id = models.CharField(max_length=50, null=True, blank=True)
    shipping = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(2.00)
    )
    coupon = models.OneToOneField(
        Coupon, on_delete=models.SET_NULL, related_name="order", null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"order id:{self.id}"

    def calculate_final_price(self):
        order_items = self.orderItems.select_related("product")
        final_price = sum(
            item.product.discounted_price * item.quantity for item in order_items
        )
        if self.coupon:
            self.final_price = self.shipping + final_price * (
                1 - self.coupon.percent / 100
            )
        else:
            self.final_price = self.shipping + final_price


class OrderItem(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="orderItems",
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.order}, {self.product}"


# class Transaction(BaseModel):
#     class StatusChoice(models.IntegerChoices):
#         PENDING = 1, "PENDING"
#         PAID = 2, "PAID"
#         FAILED = 3, "FAILED"
#         DONE = 4, "DONE"
#         CANCEL = 5, "CANCEL"

#     order = models.ForeignKey(
#         Order,
#         on_delete=models.SET_NULL,
#         related_name="transactions",
#         null=True,
#         blank=True,
#     )
#     status = models.IntegerField(choices=StatusChoice.choices, default=1)

#     class Meta:
#         verbose_name_plural = "transactions"

#     def __str__(self):
#         return f"order {self.order} {self.final_price}"
