# Generated by Django 5.1.7 on 2025-04-10 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('closet', '0001_initial'),
        ('user_management', '0003_profile_bio_profile_followers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Showroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='showroomimages/')),
                ('is_public', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_showrooms', to='user_management.profile')),
            ],
        ),
        migrations.CreateModel(
            name='ShowroomCollaborator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_invited', models.DateTimeField(auto_now_add=True)),
                ('date_accepted', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('collaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.profile')),
                ('invited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_collab_invites', to='user_management.profile')),
                ('showroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showrooms.showroom')),
            ],
            options={
                'unique_together': {('showroom', 'collaborator')},
            },
        ),
        migrations.AddField(
            model_name='showroom',
            name='collaborators',
            field=models.ManyToManyField(blank=True, related_name='collaborated_showrooms', through='showrooms.ShowroomCollaborator', to='user_management.profile'),
        ),
        migrations.CreateModel(
            name='ShowroomFollower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_followed', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.profile')),
                ('showroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showrooms.showroom')),
            ],
            options={
                'unique_together': {('showroom', 'profile')},
            },
        ),
        migrations.AddField(
            model_name='showroom',
            name='followers',
            field=models.ManyToManyField(related_name='followed_showrooms', through='showrooms.ShowroomFollower', to='user_management.profile'),
        ),
        migrations.CreateModel(
            name='ShowroomOutfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('outfit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='closet.outfit')),
                ('showroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showrooms.showroom')),
            ],
            options={
                'unique_together': {('showroom', 'outfit')},
            },
        ),
        migrations.AddField(
            model_name='showroom',
            name='outfits',
            field=models.ManyToManyField(related_name='included_in_showrooms', through='showrooms.ShowroomOutfit', to='closet.outfit'),
        ),
    ]
