from rest_framework import serializers
from core.utils import get_phonenumber_regex
from .models import CustomerProfile, User, Address, Customer


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[get_phonenumber_regex()])
    next = serializers.CharField(default=None)


class OtpCodeSerializer(serializers.Serializer):
    verify_code = serializers.CharField()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("province", "city", "street", "detail", "postal_code", "user", "id")


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ("gender", "shaba_number", "birthday")


class CustomerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(read_only=True, many=True)
    profile = CustomerProfileSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "national_code",
            "is_active",
            "role",
            "profile",
            "addresses",
        )
