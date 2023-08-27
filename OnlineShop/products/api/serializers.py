from rest_framework import serializers
from ..models import Product, ProductImage, Category, Discount, Comment


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image", "product")


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = (
            "title",
            "price",
            "info",
            "discount",
            "images",
            "id",
            "discounted_price",
            "slug",
            "category",
            "wish_count",
            "orders_count",
            "is_active",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "image", "slug")


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        exclude = ("created_at", "updated_at", "is_deleted")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("product", "customer", "parent_comment", "rate", "status", "content")
