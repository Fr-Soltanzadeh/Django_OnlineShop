from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where phone_number is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, phone_number, password, **extra_fields):
        """
        Create and save a user with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError(_("The phone_number must be set"))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        """
        Create and save a SuperUser with the given phone_number and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone_number, password, **extra_fields)


class CustomerManager(BaseUserManager):
    def create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError(_("The phone_number must be set"))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.save()
        return user

    def get_queryset(self):
        return super().get_queryset().filter(role=1)