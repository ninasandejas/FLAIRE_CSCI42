from django import forms
from .models import *


class ShowroomCreateForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs=
            {'class': 'form-control', 'placeholder': 'like "Boho-chic Outfits'}))
    collaborators = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs=
            {'class': 'select2'})
    ) 
    class Meta:
        model = Showroom
        fields = ['title', 'cover_image', 'is_public', 'tags', 'collaborators']