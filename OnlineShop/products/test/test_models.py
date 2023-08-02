from django.test import TestCase
from ..models import Product, Category, Comment, ProductImage, Discount
from model_bakery import baker
from django.urls import reverse
from decimal import Decimal


class TestCategoryModel(TestCase):
    def setUp(self):
        self.category=Category.objects.create(name="dolls")

    def test_model_str(self):
        self.assertEqual(str(self.category), "dolls")


class TestProductModel(TestCase):
    def setUp(self):
        category=Category.objects.create(name="dolls")
        discount=baker.make(Discount, percent=10)
        self.product = baker.make(Product, title="girl_doll", slug="girl-doll", info="", category=category, price=30.00, discount=discount)

    def test_model_str(self):
        self.assertEqual(str(self.product), "girl_doll")

    def test_model_discounted_price(self):
        self.assertEqual(self.product.discounted_price, Decimal(27.00))

    def test_get_absolute_url(self):
        self.assertEqual(
            self.product.get_absolute_url(), reverse("product_detail", args=(self.product.slug,))
        )


class TestCommentModel(TestCase):
    def setUp(self):
        product=baker.make(Product, title="doll", info="")
        self.comment=baker.make(Comment,rate=5, product=product)

    def test_model_str(self):
        self.assertEqual(str(self.comment), "doll: 5 star")


class TestDiscountModel(TestCase):
    def setUp(self):
        self.discount=baker.make(Discount,title="Yalda", percent=10)

    def test_model_str(self):
        self.assertEqual(str(self.discount), "Yalda 10%")


class TestProductImageModel(TestCase):
    def setUp(self):
        product=baker.make(Product, title="doll", info="")
        self.image=ProductImage.objects.create(product=product)

    def test_model_str(self):
        self.assertEqual(str(self.image), f"id:{self.image.id}, {self.image.product}")
