from ..models import Product, Category, Discount, Comment
from .serializers import ProductSerializer, CategorySerializer, DiscountSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from accounts.permissions import IsAdminUserOrReadOnly
from rest_framework.viewsets import ModelViewSet
from products.pagination import ProductPagination


class ProductListCreateView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    @method_decorator(cache_page(180))
    def get(self, request, *args, **kwargs):
        self.queryset = Product.objects.all()
        if category := self.request.GET.get("category"):
            print(category)
            category = Category.objects.get(slug=category)

            self.queryset = self.queryset.filter(category=category)
        if search_phrase := self.request.GET.get("search"):
            self.queryset = self.queryset.filter(title__icontains=search_phrase)
        return self.list(request, *args, **kwargs)


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    authentication_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

    def list(self, request):
        queryset = Category.objects.filter(parent_category__isnull=True)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class DiscountViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = []
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
