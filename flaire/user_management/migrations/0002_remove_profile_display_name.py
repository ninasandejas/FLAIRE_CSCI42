# Generated by Django 5.1.7 on 2025-03-16 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='display_name',
        ),
    ]
