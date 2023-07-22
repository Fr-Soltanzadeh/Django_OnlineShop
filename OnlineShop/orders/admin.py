from django.contrib import admin
from .models import Order, Transaction, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 3


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "status",
    )
    search_fields = ("customer",)
    list_filter = ("status",)
    list_editable = ("status",)
    inlines = [
        OrderItemInline,
    ]
    list_per_page = 10


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("order", "final_price")
    search_fields = ("order",)
    list_per_page = 10


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity")
    list_filter = ("updated_at", "product")
    autocomplete_fields = ("product",)
    list_per_page = 10
