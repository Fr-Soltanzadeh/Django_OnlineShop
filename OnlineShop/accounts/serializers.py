from rest_framework import serializers
from core.utils import get_phonenumber_regex


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[get_phonenumber_regex()])
    next = serializers.CharField(default=None)

class OtpCodeSerializer(serializers.Serializer):
    verify_code = serializers.CharField()
    
