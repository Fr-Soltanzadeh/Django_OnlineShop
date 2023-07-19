# Generated by Django 4.2.3 on 2023-07-18 09:50

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=100)),
                (
                    "image",
                    models.ImageField(
                        default="static/images/category_default.png",
                        upload_to="images/",
                    ),
                ),
                ("slug", models.SlugField()),
                (
                    "parent_category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="categories",
                        to="products.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Discount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("percent", models.PositiveIntegerField()),
                ("quantity", models.PositiveIntegerField()),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("title", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "Discounts",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("title", models.CharField(max_length=150)),
                ("price", models.DecimalField(decimal_places=2, max_digits=2)),
                (
                    "image",
                    models.ImageField(
                        default="static/images/product_default.png", upload_to="images/"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("info", ckeditor.fields.RichTextField()),
                ("slug", models.SlugField()),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="products.category",
                    ),
                ),
                (
                    "discount",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        related_name="products",
                        to="products.discount",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("content", models.CharField(max_length=500)),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "PENDING"), (2, "APPROVED"), (3, "REJECTED")],
                        default=1,
                    ),
                ),
                (
                    "rate",
                    models.IntegerField(
                        choices=[
                            (1, "1 STAR"),
                            (2, "2 STAR"),
                            (3, "3 STAR"),
                            (4, "4 STAR"),
                            (5, "5 STAR"),
                        ]
                    ),
                ),
                (
                    "parent_comment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="comments",
                        to="products.comment",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="products.product",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        default="anonymous",
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Comments",
            },
        ),
    ]