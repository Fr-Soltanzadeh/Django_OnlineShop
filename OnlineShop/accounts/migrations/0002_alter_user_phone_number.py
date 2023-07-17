# Generated by Django 4.2.3 on 2023-07-17 14:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(
                max_length=14,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="invalid phone number",
                        regex="^(\\+?|0*)(98)?9[\\d-]{9,}$",
                    )
                ],
                verbose_name="phone number",
            ),
        ),
    ]
