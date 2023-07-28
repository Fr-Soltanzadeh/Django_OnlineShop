from rest_framework import serializers
from .models import Product, ProductImage, Category


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image", "product")

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ("title","price","info","discount","images","id")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name","image","slug")
