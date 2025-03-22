from django.db import models
from user_management.models import Profile

# from django.forms import CharField


class ClothingItem(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="clothing_items", null=True
    )
    image = models.ImageField(upload_to="clothingitemimages/", blank=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_updated = models.DateTimeField(auto_now=True, null=False)
    brand = models.CharField(max_length=100, null=True)
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
            ("GOLD", "GOld"),
            ("MULTI", "Multicolor"),
        ],
        default="BLACK",
        null=False,
        blank=False,
    )


class Outfit(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="outfits", null=True
    )
    image = models.ImageField(upload_to="outfitimages/", blank=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_updated = models.DateTimeField(auto_now=True, null=False)
