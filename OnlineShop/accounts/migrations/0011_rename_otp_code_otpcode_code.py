# Generated by Django 4.2.3 on 2023-07-19 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_rename_code_otpcode_otp_code"),
    ]

    operations = [
        migrations.RenameField(
            model_name="otpcode",
            old_name="otp_code",
            new_name="code",
        ),
    ]