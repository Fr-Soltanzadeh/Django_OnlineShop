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
    autocomplete_fields = ("category",)
    list_filter = ("category", "is_active")
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("parent_category",)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        CategoryInline,
    ]
    list_per_page = 10


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "status", "rate")
    search_fields = ("product",)
    list_filter = ("product",)
    list_editable = ("status",)
    list_per_page = 10


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("title", "percent", "start_time", "end_time", "is_active")
    search_fields = ("title",)
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    list_per_page = 10
