# Generated by Django 4.2.3 on 2023-07-19 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_otpcode"),
    ]

    operations = [
        migrations.RenameField(
            model_name="otpcode",
            old_name="code",
            new_name="otp_code",
        ),
    ]