from django.shortcuts import render
from django.views import View


class CartView(View):
    template_name="cart.html"
    def get(self, request):
        render(request, template_name)
