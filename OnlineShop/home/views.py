from django.shortcuts import render
from django.views import View
from products.models import Category


class HomeView(View):
    template_name = "index.html"
    
    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name, context={"categories":categories})
