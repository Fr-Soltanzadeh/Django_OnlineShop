from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User
from core.utils import get_phonenumber_regex


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("phone_number",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("phone_number",)


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        label="",
        validators=[get_phonenumber_regex()],
        widget=forms.TextInput(attrs={"placeholder": "Phone Number"}),
    )


class VerifyCodeForm(forms.Form):
    verify_code = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Verification Code"})
    )
