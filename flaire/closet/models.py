from django.db import models

# from django.forms import CharField

# from user_management.models import Profile


class ClothingItem(models.Model):
    image = models.ImageField(upload_to="clothingitemimages/", null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_updated = models.DateTimeField(auto_now=True, null=False)
    brand = models.CharField(max_length=100, null=True)

    CATEGORY_CHOICES = [
        ("TOP", "Top"),
        ("BOTTOM", "Bottom"),
        ("DRESS", "Dress"),
        ("JEWELRY", "Jewelry"),
        ("BAG", "Bag"),
        ("SHOES", "Shoes"),
    ]

    COLOR_CHOICES = [
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
    ]


class Outfit(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    date_updated = models.DateTimeField(auto_now=True, null=False)
