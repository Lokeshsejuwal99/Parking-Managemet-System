# Generated by Django 5.0.1 on 2024-02-06 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Vehicle", "0006_remove_vehicle_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_admin",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="is_user",
            field=models.BooleanField(default=False),
        ),
    ]
