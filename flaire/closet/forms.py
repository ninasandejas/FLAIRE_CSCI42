from django import forms

from .models import *


class AddClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = ["name", "image", "brand", "category", "color"]


class SaveOutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ["caption", "tags"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["entry"]
        labels = {"entry": ""}
