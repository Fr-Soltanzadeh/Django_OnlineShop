from django.contrib import admin
from .models import Product, Discount, Comment, Category, ProductImage


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 3

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_per_page = 10

    
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
    inlines = [ProductImageInline]
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
    list_display = ("product", "customer", "status", "rate")
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
