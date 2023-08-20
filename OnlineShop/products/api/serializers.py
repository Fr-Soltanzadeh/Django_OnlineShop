from rest_framework import serializers
from ..models import Product, ProductImage, Category, Discount, Comment


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image", "product")


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    wish_count = serializers.SerializerMethodField()
    orders_count = serializers.SerializerMethodField()

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

    def get_discounted_price(self, product):
        return (
            product.price
            * (100 - (product.discount.percent if product.discount else 0))
            / 100
        )

    def get_category(self, product):
        return product.category.name

    def get_wish_count(self, product):
        return product.wish_list.count()

    def get_orders_count(self, product):
        return product.orders.count()


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
        fields = ('product', 'customer', 'parent_comment', 'rate', 'status', 'content')
    