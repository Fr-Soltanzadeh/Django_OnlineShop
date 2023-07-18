from django.contrib import admin
from .models import Product, Discount, Comment, Category


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
    )
    search_fields = ("title", "category")
    autocomplete_fields("category")
    list_filter = ("category", "is_active")
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("parent_category",)
    inlines = [CategoryInline,]
    list_per_page = 10