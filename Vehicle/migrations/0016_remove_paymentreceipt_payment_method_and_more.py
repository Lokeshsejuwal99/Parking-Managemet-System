# Generated by Django 5.0.1 on 2024-02-28 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Vehicle", "0015_billnumber"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paymentreceipt",
            name="payment_method",
        ),
        migrations.RemoveField(
            model_name="paymentreceipt",
            name="receipt_image",
        ),
    ]
