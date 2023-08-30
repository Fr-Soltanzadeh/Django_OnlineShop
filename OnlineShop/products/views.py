from django.shortcuts import render
from django.views import View


class ProductListView(View):
    template_name = "products/product_list.html"

    def get(self, request):
        if category := request.GET.get("category"):
            return render(request, self.template_name, context={"category": category})
        return render(request, self.template_name)


class ProductDetailView(View):
    template_name = "products/product_details.html"

    def get(self, request, slug):
        return render(request, self.template_name, context={"slug": slug})


class OfferedProductListView(View):
    template_name = "products/offer.html"

    def get(self, request):
        return render(request, self.template_name)


class WishListProductView(View):
    template_name = "products/wishlist.html"

    def get(self, request):
        return render(request, self.template_name)
