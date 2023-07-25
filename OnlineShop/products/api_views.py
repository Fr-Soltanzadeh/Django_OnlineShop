from .models import Product, Category
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class ProductListByCategoryApiView(APIView):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductListApiView(APIView):

    def get(self, request):
        search_phrase = request.GET.get("search")
        if not search_phrase:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(title__icontains = search_phrase)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailApiView(APIView):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)