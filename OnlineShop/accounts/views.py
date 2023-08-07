from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import logout
from .forms import LoginForm, VerifyCodeForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)


class LoginOrRegisterView(View):
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("profile"))
        form = LoginForm()
        return render(request, self.template_name, {"form": form})


class VerifyCodeView(View):
    template_name = "accounts/verify_code.html"

    def get(self, request):
        if request.user.is_authenticated:
            # print("111111111111111111111111111111111111111")
            return HttpResponseRedirect(reverse("profile"))
        elif not request.session.get("login_info"):
            # print("222222222222222222222222222222222")
            print(request.session.get("login_info"))
            return HttpResponseRedirect(reverse("login"))
        # print("333333333333333333333333333333")
        form = VerifyCodeForm()
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class ProfileView(View):
    template_name = "accounts/profile.html"

    def get(self, request):
        return render(request, self.template_name)

