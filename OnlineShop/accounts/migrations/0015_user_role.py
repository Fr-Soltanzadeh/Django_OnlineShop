# Generated by Django 4.2.3 on 2023-07-27 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0014_remove_address_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.IntegerField(
                choices=[
                    (0, "ADMIN"),
                    (1, "CUSTOMER"),
                    (2, "STAFF"),
                    (3, "PRODUCT_MANAGER"),
                ],
                default=1,
            ),
        ),
    ]
