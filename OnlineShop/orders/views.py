from django.shortcuts import render
from django.views import View


class CheckoutView(View):
    template_name = "orders/checkout.html"

    def get(self, request):
        return render(request, self.template_name)
