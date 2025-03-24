from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs=
        {'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=
        {'class': 'form-control', 'placeholder': 'password'}))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'email'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'password'
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["password2"]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    

class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture", "bio"]
        widgets = {
            "bio": forms.Textarea(attrs={"placeholder": "Tell us something about yourself...", "rows": 3}),
            "maxlength": "150",
            "style": "resize: none;"
        }

    def clean(self):
        cleaned_data = super().clean()
        profile_picture = cleaned_data.get("profile_picture")
        bio = cleaned_data.get("bio")

        if not profile_picture and not bio:
            raise forms.ValidationError("You must fill in at least one field (profile picture or bio).")

        return cleaned_data