from django.shortcuts import render
from django.views import View


class ProductListView(View):
    template_name = "product_list_by_category.html"
    
    def get(self, request, slug):
        return render(request, self.template_name, context={"slug": slug})
