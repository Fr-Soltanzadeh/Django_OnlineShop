from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "phone_number",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "date_joined",
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
    ordering = ("first_name","last_name")


admin.site.register(User, CustomUserAdmin)
