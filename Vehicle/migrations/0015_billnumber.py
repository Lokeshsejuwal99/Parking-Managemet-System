# Generated by Django 5.0.1 on 2024-02-26 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Vehicle", "0014_parkinglot_date_delete_dailydata"),
    ]

    operations = [
        migrations.CreateModel(
            name="BillNumber",
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
                ("bill_no", models.IntegerField(unique=True)),
            ],
        ),
    ]
