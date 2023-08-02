from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Product
from core.utils import get_phonenumber_regex


class Order(BaseModel):
    class StatusChoice(models.IntegerChoices):
        PENDING = 1, "PENDING"
        CONFIRMED = 2, "CONFIRMED"
        SENDING = 3, "SENDING"
        DELIVERED = 4, "DELIVERED"
        CANCEL = 5, "CANCEL"

    status = models.IntegerField(choices=StatusChoice.choices, default=1)
    customer = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="orders", null=True
    )
    province = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    detail = models.CharField(max_length=300, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=2, decimal_places=2, null=True, blank=True
    )
    final_price = models.DecimalField(
        max_digits=2, decimal_places=2, null=True, blank=True
    )
    receiver_fullname = models.CharField(max_length=100, null=True, blank=True)
    receiver_phone_number = models.CharField(
        max_length=14, validators=[get_phonenumber_regex()], null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"order id:{self.id}"


class Transaction(BaseModel):
    class StatusChoice(models.IntegerChoices):
        PENDING = 1, "PENDING"
        PAID = 2, "PAID"
        FAILED = 3, "FAILED"
        DONE = 4, "DONE"
        CANCEL = 5, "CANCEL"

    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        related_name="transactions",
        null=True,
        blank=True,
    )
    final_price = models.DecimalField(
        max_digits=2, decimal_places=2, null=True, blank=True
    )
    status = models.IntegerField(choices=StatusChoice.choices, default=1)

    class Meta:
        verbose_name_plural = "transactions"

    def __str__(self):
        return f"order {self.order} {self.final_price}"


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
    price = models.DecimalField(max_digits=2, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.order}, {self.product}"
