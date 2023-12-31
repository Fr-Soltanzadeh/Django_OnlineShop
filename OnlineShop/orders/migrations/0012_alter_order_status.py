# Generated by Django 4.2.3 on 2023-08-09 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0011_alter_order_final_price_alter_order_shipping_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.IntegerField(
                choices=[
                    (1, "PENDING"),
                    (2, "PAID"),
                    (3, "PAYMENT_FAILED"),
                    (4, "SENDING"),
                    (5, "DELIVERED"),
                    (6, "CANCEL"),
                ],
                default=1,
            ),
        ),
    ]
