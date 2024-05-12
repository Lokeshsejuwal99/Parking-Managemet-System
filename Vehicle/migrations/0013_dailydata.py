# Generated by Django 5.0.1 on 2024-02-23 13:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vehicle', '0012_parkinglot_total_reserved_spaces'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('available_spaces', models.PositiveIntegerField(default=500)),
                ('reserved_spaces', models.PositiveIntegerField(default=0)),
                ('parking_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vehicle.parkinglot')),
            ],
        ),
    ]