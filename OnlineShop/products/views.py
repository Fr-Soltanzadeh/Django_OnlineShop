from django.shortcuts import render
from django.views import View


class ProductListView(View):
    template_name = "products/product_list.html"

    def get(self, request):
        return render(request, self.template_name)


class ProductListByCategoryView(View):
    template_name = "products/product_list_by_category.html"

    def get(self, request, slug):
        return render(request, self.template_name, context={"slug": slug})


class ProductDetailView(View):
    template_name = "products/product_details.html"

    def get(self, request, slug):
        return render(request, self.template_name, context={"slug": slug})
