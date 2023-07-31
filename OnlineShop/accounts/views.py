from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, VerifyCodeForm
from django.utils.translation import gettext_lazy as _
from .utils import send_otp_code
import random
from .models import User, OtpCode, CustomerProfile
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)

class LoginOrRegisterView(View):
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            otp_code = random.randint(1000, 9999)
            send_otp_code(phone_number, otp_code)
            if  OtpCode.objects.filter(phone_number=phone_number).exists():
                OtpCode.objects.get(phone_number=phone_number).delete()
            OtpCode.objects.create(phone_number=phone_number, code=otp_code)
            request.session["login_info"] = {
                "phone_number": phone_number,
                "redirect_to": request.POST.get("next", ""),
            }
            messages.success(
                request,
                f"A verification code has been sent to your phone number",
            )
            return redirect("verify_code")
        return render(request, self.template_name, {"form": form})


class VerifyCodeView(View):
    template_name = "accounts/verify_code.html"

    def get(self, request):
        form = VerifyCodeForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            phone_number = request.session["login_info"]["phone_number"]
            otp_code = OtpCode.objects.get(phone_number=phone_number)
            if form.cleaned_data["verify_code"] == str(otp_code.code):
                if not User.objects.filter(phone_number=phone_number).exists():
                    user = User.objects.create(phone_number=phone_number)
                else:
                    user = User.objects.get(phone_number=phone_number)
                redirect_to = request.session["login_info"]["redirect_to"]
                login(request, user)
                otp_code.delete()
                messages.success(request, "You have successfully logged in.")
                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                return HttpResponseRedirect(reverse("profile", args=(user.id,)))
        messages.error(
            request,
            "The entered code is not correct. Try again",
        )
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
