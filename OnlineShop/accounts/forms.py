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
    phone_number = forms.CharField(label="Phone Number", validators=[get_phonenumber_regex()])
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
