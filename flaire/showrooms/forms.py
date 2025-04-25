from django import forms
from .models import *


class ShowroomCreateForm(forms.ModelForm):
    # assume for now that they can invite any user (not just people that they are following or being followed)
    collaborators = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.all(),
        required=False,
       widget=forms.SelectMultiple(attrs={'class': 'select2'})
    ) 
    outfits = forms.ModelMultipleChoiceField(
        queryset=Outfit.objects.none(),  # we will just override in view
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Showroom
        fields = ['title', 'cover_image', 'tags', 'is_public', 'collaborators', 'outfits']