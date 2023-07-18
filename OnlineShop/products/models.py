from django.db import models
from core.models import BaseModel


class Category(ModelInfo):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        related_name="categories",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="images/", default="static/images/category_default.png")
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(BaseModel):

    title = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=2)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="images/", default="static/images/product_default.png")
    is_active = models.BooleanField(default=True)
    info = RichTextField()
    discount = models.ForeignKey("Discount", on_delete=models.SET_DEFAULT, default=0, related_name="products")
    slug = models.SlugField()
    
    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title
