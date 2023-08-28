from ..models import Product, Category, Discount, Comment
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    DiscountSerializer,
    CommentSerializer,
)
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.postgres.search import TrigramSimilarity
from accounts.permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from rest_framework.viewsets import ModelViewSet
from products.pagination import ProductPagination
from accounts.authentication import LoginAuthentication

# from django.core.cache import cache


class ProductListCreateView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    @method_decorator(cache_page(180))
    def get(self, request, *args, **kwargs):
        self.queryset = Product.objects.select_related(
            "category", "discount"
        ).prefetch_related("images", "comments")
        if category := self.request.GET.get("category"):
            category = Category.objects.get(slug=category)
            self.queryset = self.queryset.filter(category=category)
        if search_phrase := self.request.GET.get("search"):
            self.queryset = (
                self.queryset.annotate(
                    similarity=TrigramSimilarity("title", search_phrase)
                )
                .filter(similarity__gt=0.1)
                .order_by("-similarity")
            )
            # self.queryset = self.queryset.filter(title__icontains=search_phrase)
        return self.list(request, *args, **kwargs)


class OfferedProductListView(generics.ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    @method_decorator(cache_page(180))
    def get(self, request, *args, **kwargs):
        self.queryset = (
            Product.objects.select_related("category", "discount")
            .prefetch_related("images", "comments")
            .filter(is_active=True, discount__isnull=False, discount__is_active=True)
        )
        return self.list(request, *args, **kwargs)


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    authentication_classes = []
    queryset = Product.objects.select_related("category", "discount").prefetch_related(
        "images", "comments"
    )
    serializer_class = ProductSerializer
    lookup_field = "slug"


class CommentListCreateAPIView(APIView):
    authentication_classes = [LoginAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.select_related("product", "customer").filter(
            product=request.GET.get("product_pk")
        )
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None, *args, **kwargs):
        data = request.data.copy()
        data["customer"] = request.user.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [LoginAuthentication]
    queryset = Comment.objects.select_related("product", "customer")
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


# todo cashe in which redis db
