from ..models import Product, Category, Discount, Comment
from .serializers import ProductSerializer, CategorySerializer, DiscountSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from accounts.permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from rest_framework.viewsets import ModelViewSet
from products.pagination import ProductPagination
from accounts.authentication import LoginAuthentication


class ProductListCreateView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    @method_decorator(cache_page(180))
    def get(self, request, *args, **kwargs):
        self.queryset = Product.objects.all()
        if category := self.request.GET.get("category"):
            category = Category.objects.get(slug=category)
            self.queryset = self.queryset.filter(category=category)
        if search_phrase := self.request.GET.get("search"):
            self.queryset = self.queryset.filter(title__icontains=search_phrase)
        return self.list(request, *args, **kwargs)


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    authentication_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

    
class CommentListCreateAPIView(APIView):
    authentication_classes = [LoginAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(product=request.GET.get('product_pk'))
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None, *args, **kwargs):
        data=request.data.copy()
        data['customer']=request.user.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [LoginAuthentication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    authentication_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

    @method_decorator(cache_page(180))
    def list(self, request):
        queryset = Category.objects.filter(parent_category__isnull=True)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class DiscountViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
