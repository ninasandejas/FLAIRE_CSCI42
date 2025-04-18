from django import forms

from .models import *


class AddClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = ["name", "image", "brand", "category", "color"]
