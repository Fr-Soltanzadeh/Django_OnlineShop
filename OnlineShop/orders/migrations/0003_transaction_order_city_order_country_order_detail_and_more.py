# Generated by Django 4.2.3 on 2023-07-20 09:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_alter_order_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
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
                (
                    "final_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=2, null=True
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "PENDING"),
                            (2, "PAID"),
                            (3, "FAILED"),
                            (4, "DONE"),
                            (5, "CANCEL"),
                        ],
                        default=1,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "transactions",
            },
        ),
        migrations.AddField(
            model_name="order",
            name="city",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="country",
            field=django_countries.fields.CountryField(
                blank=True, max_length=2, null=True
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="detail",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="final_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=2, null=True
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="postal_code",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="province",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="receiver_fullname",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="receiver_phone_number",
            field=models.CharField(
                blank=True,
                max_length=14,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="invalid phone number",
                        regex="^(\\+?|0*)(98)?9[\\d-]{9,}$",
                    )
                ],
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="street",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=2, null=True
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=2, null=True
            ),
        ),
        migrations.DeleteModel(
            name="Receipt",
        ),
        migrations.AddField(
            model_name="transaction",
            name="order",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="transactions",
                to="orders.order",
            ),
        ),
    ]