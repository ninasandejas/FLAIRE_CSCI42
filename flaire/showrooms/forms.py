from django import forms
from .models import *


class ShowroomCreateForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs=
            {'class': 'form-control', 'placeholder': 'like "Boho-chic Outfits'}))
    collaborators = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs=
            {'class': 'select2'})
    ) 

    class Meta:
        model = Showroom
        fields = ['title', 'cover_image', 'is_public', 'tags', 'collaborators']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ShowroomCreateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['collaborators'].queryset = Profile.objects.exclude(user=user)
        self.fields['tags'].help_text = ''
        self.fields['tags'].widget.attrs.update({
            'placeholder': 'Add up to 3 tags, separated by commas',
            'style': 'width: 30%;'})