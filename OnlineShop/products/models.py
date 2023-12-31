from django.db import models
from core.models import BaseModel
from ckeditor.fields import RichTextField
from accounts.models import User
from django.urls import reverse


class Category(BaseModel):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        related_name="categories",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to="images/", default="images/category_default.png"
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(BaseModel):
    title = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    info = RichTextField()
    discount = models.ForeignKey(
        "Discount",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products",
    )
    slug = models.SlugField(unique=True)
    quantity = models.PositiveIntegerField()
    wish_list = models.ManyToManyField(User, related_name="wish_list", blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", args=(self.slug,))

    @property
    def discounted_price(self):
        return (
            self.price * (100 - self.discount.percent) / 100
            if self.discount
            else self.price
        )

    @property
    def orders_count(self):
        return self.orders.count()

    @property
    def wish_count(self):
        return self.wish_list.count()

    @property
    def rate(self):
        return (
            self.comments.aggregate(models.Avg("rate"))["rate__avg"]
            if self.comments.exists()
            else None
        )


class ProductImage(BaseModel):
    image = models.ImageField(
        upload_to="images/", default="static/images/product_default.png"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )

    class Meta:
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"id:{self.id}, {self.product}"


class Comment(BaseModel):
    class StatusChoices(models.IntegerChoices):
        PENDING = 1, "PENDING"
        APPROVED = 2, "APPROVED"
        REJECTED = 3, "REJECTED"

    class RateChoices(models.IntegerChoices):
        star1 = 1, "1 STAR"
        star2 = 2, "2 STAR"
        star3 = 3, "3 STAR"
        star4 = 4, "4 STAR"
        star5 = 5, "5 STAR"

    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="comments"
    )
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="comments"
    )
    content = models.CharField(max_length=500)
    parent_comment = models.ForeignKey(
        "Comment",
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
        blank=True,
    )
    status = models.IntegerField(choices=StatusChoices.choices, default=1)
    rate = models.IntegerField(choices=RateChoices.choices)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.product}: {self.rate} star"


class Discount(BaseModel):
    percent = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Discounts"

    def __str__(self):
        return f"{self.title} {self.percent}%"
