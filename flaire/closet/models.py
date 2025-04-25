import os

import tinify
from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager
from user_management.models import Profile


class ClothingItem(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="clothing_items", null=True
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="clothingitemimages/", blank=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_updated = models.DateTimeField(auto_now=True, null=False)
    brand = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(
        max_length=10,
        choices=[
            ("TOP", "Top"),
            ("BOTTOM", "Bottom"),
            ("DRESS", "Dress"),
            ("JEWELRY", "Jewelry"),
            ("BAG", "Bag"),
            ("SHOES", "Shoes"),
        ],
        default="TOP",
        null=True,
        blank=False,
    )
    color = models.CharField(
        max_length=10,
        choices=[
            ("BLACK", "Black"),
            ("GREY", "Grey"),
            ("WHITE", "White"),
            ("BROWN", "Brown"),
            ("CREAM", "Cream"),
            ("YELLOW", "Yellow"),
            ("RED", "Red"),
            ("BURGUNDY", "Burgundy"),
            ("ORANGE", "Orange"),
            ("PINK", "Pink"),
            ("PURPLE", "Purple"),
            ("BLUE", "Blue"),
            ("NAVY", "Navy"),
            ("GREEN", "Green"),
            ("KHAKI", "Khaki"),
            ("SILVER", "Silver"),
            ("GOLD", "Gold"),
            ("MULTI", "Multicolor"),
        ],
        default="BLACK",
        null=False,
        blank=False,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Only try to compress if it's a PNG and the file exists
        if self.image and self.image.name.endswith(".png"):
            image_path = self.image.path
            if os.path.exists(image_path):
                try:
                    tinify.key = settings.TINIFY_API_KEY
                    source = tinify.from_file(image_path)
                    source.to_file(image_path)
                except tinify.Error as e:
                    print("❌ TinyPNG compression failed:", e)


class Outfit(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="outfits", null=True
    )
    image = models.ImageField(upload_to="outfitimages/", blank=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_updated = models.DateTimeField(auto_now=True, null=False)
    # for the outfit post
    caption = models.CharField(max_length=2200, null=True, blank=True)
    listed_items = models.ManyToManyField(
        ClothingItem, related_name="outfit_items", blank=True
    )
    tags = TaggableManager(blank=True)
    likes = models.ManyToManyField(Profile, related_name="liked_outfits", blank=True)


class Comment(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="authored_comments",
    )
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    entry = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_updated = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        ordering = ["date_created"]
        verbose_name_plural = "Comments"
