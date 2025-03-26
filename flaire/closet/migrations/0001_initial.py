# Generated by Django 5.1.7 on 2025-03-22 07:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_management', '0003_profile_bio_profile_followers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClothingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='clothingitemimages/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('brand', models.CharField(max_length=100, null=True)),
                ('category', models.CharField(choices=[('TOP', 'Top'), ('BOTTOM', 'Bottom'), ('DRESS', 'Dress'), ('JEWELRY', 'Jewelry'), ('BAG', 'Bag'), ('SHOES', 'Shoes')], default='TOP', max_length=10, null=True)),
                ('color', models.CharField(choices=[('BLACK', 'Black'), ('GREY', 'Grey'), ('WHITE', 'White'), ('BROWN', 'Brown'), ('CREAM', 'Cream'), ('YELLOW', 'Yellow'), ('RED', 'Red'), ('BURGUNDY', 'Burgundy'), ('ORANGE', 'Orange'), ('PINK', 'Pink'), ('PURPLE', 'Purple'), ('BLUE', 'Blue'), ('NAVY', 'Navy'), ('GREEN', 'Green'), ('KHAKI', 'Khaki'), ('SILVER', 'Silver'), ('GOLD', 'GOld'), ('MULTI', 'Multicolor')], default='BLACK', max_length=10)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clothing_items', to='user_management.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='outfitimages/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outfits', to='user_management.profile')),
            ],
        ),
    ]
