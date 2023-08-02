from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, CustomerProfile, Address, OtpCode, Customer


class ProfileInline(admin.TabularInline):
    model = CustomerProfile
    extra = 1


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("phone_number", "is_staff", "is_active", "fullname")
    list_filter = (
        "created_at",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                    "is_superuser",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("phone_number",)
    ordering = ("first_name", "last_name")
    inlines = [AddressInline]
    list_per_page = 10


admin.site.register(User, CustomUserAdmin)


@admin.register(Customer)
class CustomerAdmin(CustomUserAdmin):
    list_display = ("phone_number", "fullname")
    list_filter = (
        "created_at",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("phone_number",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "first_name",
                    "last_name",
                    "role",
                    "national_code",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "is_active",
                    "first_name",
                    "last_name",
                    "role",
                    "national_code",
                ),
            },
        ),
    )
    inlines = [ProfileInline, AddressInline]
    list_per_page = 10


@admin.register(CustomerProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "gender",
    )
    search_fields = ("phone_number",)
    list_filter = ("gender", "birthday")
    radio_fields = {"gender": admin.HORIZONTAL}
    list_per_page = 10


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "city",
        "street",
    )
    search_fields = ("city", "street")
    list_filter = ("city", "street")
    list_per_page = 10


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = (
        "phone_number",
        "code",
        "created_at",
    )
    search_fields = ("phone_number",)
    list_filter = ("created_at",)
    list_per_page = 10
