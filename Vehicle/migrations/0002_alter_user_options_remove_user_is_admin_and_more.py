# Generated by Django 5.0.1 on 2024-02-04 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Vehicle", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "user", "verbose_name_plural": "users"},
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_admin",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_cashier",
        ),
    ]
