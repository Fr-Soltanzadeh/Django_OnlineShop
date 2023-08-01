from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from .forms import LoginForm, VerifyCodeForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)


class LoginOrRegisterView(View):
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})


class VerifyCodeView(View):
    template_name = "accounts/verify_code.html"

    def get(self, request):
        form = VerifyCodeForm()
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class ProfileView(LoginRequiredMixin, View):
    login_url = "/login/"
    template_name = "accounts/profile.html"

    def get(self, request):
        return render(request, self.template_name)
