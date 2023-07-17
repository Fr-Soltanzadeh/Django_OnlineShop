from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from core.utils import get_phonenumber_regex



class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        _("phone number"), max_length=14, unique=True, validators=[get_phonenumber_regex()]
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.first_name + self.last_name