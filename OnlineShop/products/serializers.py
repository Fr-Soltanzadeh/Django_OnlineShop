from rest_framework import serializers
from .models import Product, ProductImage, Category


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image", "product")

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    discounted_price = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ("title","price","info","discount","images","id","discounted_price","slug")

    def get_discounted_price(self, product):
        return product.price*(100-(product.discount.percent if product.discount else 0))/100

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name","image","slug")
