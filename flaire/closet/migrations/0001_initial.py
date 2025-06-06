# Generated by Django 5.1.7 on 2025-04-22 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClothingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(upload_to='clothingitemimages/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(choices=[('TOP', 'Top'), ('BOTTOM', 'Bottom'), ('DRESS', 'Dress'), ('JEWELRY', 'Jewelry'), ('BAG', 'Bag'), ('SHOES', 'Shoes')], default='TOP', max_length=10, null=True)),
                ('color', models.CharField(choices=[('BLACK', 'Black'), ('GREY', 'Grey'), ('WHITE', 'White'), ('BROWN', 'Brown'), ('CREAM', 'Cream'), ('YELLOW', 'Yellow'), ('RED', 'Red'), ('BURGUNDY', 'Burgundy'), ('ORANGE', 'Orange'), ('PINK', 'Pink'), ('PURPLE', 'Purple'), ('BLUE', 'Blue'), ('NAVY', 'Navy'), ('GREEN', 'Green'), ('KHAKI', 'Khaki'), ('SILVER', 'Silver'), ('GOLD', 'Gold'), ('MULTI', 'Multicolor')], default='BLACK', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Comments',
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='outfitimages/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('caption', models.CharField(blank=True, max_length=2200, null=True)),
            ],
        ),
    ]
