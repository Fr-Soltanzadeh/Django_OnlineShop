from .models import Product, Category
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions


class ProductListByCategoryApiView(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes=[]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs['slug'])
        self.queryset = self.queryset.filter(category=category)   
        return self.list(request, *args, **kwargs)


class ProductListApiView(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes=[]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get(self, request, *args, **kwargs):
        search_phrase = request.GET.get("search")
        if search_phrase:
            self.queryset = self.queryset.filter(title__icontains = search_phrase)    
        return self.list(request, *args, **kwargs)


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes=[]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field= "slug"


# class ProductListByCategoryApiView(APIView):
#     def get(self, request, slug, format=None):
#         category = Category.objects.get(slug=slug)
#         products = Product.objects.filter(category=category)
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)


# class ProductListApiView(APIView):
#     def get(self, request, format=None):
#         search_phrase = request.GET.get("search")
#         if not search_phrase:
#             products = Product.objects.all()
#         else:
#             products = Product.objects.filter(title__icontains = search_phrase)
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)