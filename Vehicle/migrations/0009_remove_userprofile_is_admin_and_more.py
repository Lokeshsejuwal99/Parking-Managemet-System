# Generated by Django 5.0.1 on 2024-02-06 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Vehicle', '0008_remove_user_is_admin_remove_user_is_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_user',
        ),
    ]
