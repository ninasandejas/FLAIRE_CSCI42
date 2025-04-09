import os

import tinify
from django.conf import settings
from django.db import models
from user_management.models import Profile
from closet.models import Outfit


class Showroom(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="owner_showrooms", null=True
    )
    collaborators = models.ManyToManyField(
        Profile, related_name="showrooms", blank=True
    )
    outfits = models.ManyToManyField(Outfit, related_name="collaborator_showrooms", blank=True)
    cover_image = models.ImageField(upload_to="showroomimages/", blank=True, null=True)
    is_public = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # followers

    def __str__(self):
        return self.title