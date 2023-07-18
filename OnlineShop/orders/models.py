from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Product


class Order(BaseModel):

    class StatusChoice(models.IntegerChoices):
        PENDING = 1, "PENDING"
        CONFIRMED = 2, "CONFIRMED"
        SENDING = 3, "SENDING"
        RECIEVED = 4, "RECIEVED"
        CANCEL = 5, "CANCEL"

    status = models.IntegerField(choices=StatusChoice.choices, default=1)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="orders")

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"order id:{self.id}"


class Receipt(BaseModel):

    order = models.OneToOneField(
        Order, on_delete=models.SET_NULL, related_name="receipt", null=True, blank=True
    )
    total_price = models.DecimalField(max_digits=2, decimal_places=2)
    final_price = models.DecimalField(max_digits=2, decimal_places=2)

    class Meta:
        verbose_name_plural = "Receipts"

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
        Order, on_delete=models.CASCADE, related_name="orderItems",
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order}, {self.product}"

