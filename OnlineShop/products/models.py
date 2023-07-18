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
    image = models.ImageField(upload_to="images/", default='static/images/category_default.png')
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

