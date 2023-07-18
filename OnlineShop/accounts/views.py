from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views import View
from django.http import  HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.utils.translation import gettext_lazy as _



class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        redirect_to = request.POST.get("next", "")
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = authenticate(
                request=request, username=phone_number, password=password
            )
            if user:
                login(request, user)
                if redirect_to:
                    return HttpResponseRedirect(redirect_to)
                return redirect("login")

        error_message = _("Invalid phone number or password. Please try again.")
        return render(
            request, self.template_name, {"form": form, "error_message": error_message}
        )


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class ProfileView(View):
    def get(self, request, id):
        return HttpResponse("customer profile")