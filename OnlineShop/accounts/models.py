from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager, CustomerManager
from core.utils import get_phonenumber_regex
from core.models import BaseModel
from django.urls import reverse


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class RoleChoice(models.IntegerChoices):
        ADMIN = 0, "ADMIN"
        CUSTOMER = 1, "CUSTOMER"
        STAFF = 2, "STAFF"
        PRODUCT_MANAGER = 3, "PRODUCT_MANAGER"

    role = models.IntegerField(choices=RoleChoice.choices, default=1)
    phone_number = models.CharField(
        _("phone number"),
        max_length=14,
        unique=True,
        validators=[get_phonenumber_regex()],
    )
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_code = models.CharField(max_length=10, null=True, blank=True)
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

    class Meta:
        verbose_name_plural = "Users"


class Customer(User):
    class Meta:
        proxy = True

    objects = CustomerManager()


class CustomerProfile(BaseModel):
    class GenderChoices(models.IntegerChoices):
        MALE = 1, "MALE"
        FEMALE = 2, "FEMALE"

    gender = models.IntegerField(choices=GenderChoices.choices, default=1)
    birthday = models.DateField(null=True, blank=True)
    customer = models.OneToOneField(
        "Customer", on_delete=models.CASCADE, related_name="profile"
    )
    shaba_number = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name_plural = "Profiles"


class Address(BaseModel):
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    detail = models.CharField(max_length=300)
    postal_code = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")

    def __str__(self):
        return f"{self.street}, {self.city}, {self.province}"

    class Meta:
        verbose_name_plural = "Addresses"


class OtpCode(models.Model):
    phone_number = models.CharField(
        max_length=14, validators=[get_phonenumber_regex()], unique=True
    )
    code = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} - {self.code}"

    class Meta:
        verbose_name_plural = "OTP Codes"
