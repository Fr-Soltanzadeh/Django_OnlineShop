from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from core.utils import get_phonenumber_regex
from core.models import BaseModel



class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    phone_number = models.CharField(
        _("phone number"), max_length=14, unique=True, validators=[get_phonenumber_regex()]
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.phone_number

    @property
    def fullname(self):
        return self.first_name + " " + self.last_name


class Profile(BaseModel):
    class GenderChoices(models.IntegerChoices):
        MALE = 1, "MALE"
        FEMALE = 2, "FEMALE"
    gender = models.IntegerField(
        choices=GenderChoices.choices, default=1, null=True, blank=True
    )
    birthday = models.DateField(null=True, blank=True)
    national_code = models.IntegerField(null=True, blank=True)
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="profile")


