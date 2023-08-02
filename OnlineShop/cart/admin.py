from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 3


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("customer",)
    search_fields = ("customer",)
    inlines = [
        CartItemInline,
    ]
    list_per_page = 10


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity")
    list_filter = ("updated_at", "product")
    autocomplete_fields = ("product",)
    list_per_page = 10
