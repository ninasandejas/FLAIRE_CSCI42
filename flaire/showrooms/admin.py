from django import forms
from django.contrib import admin

from .models import Showroom, Profile, Outfit


# class ShowroomAdminForm(forms.ModelForm):
#     class Meta:
#         model = Showroom
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['collaborators'].queryset = Profile.objects.all()
#         self.fields['outfits'].queryset = Outfit.objects.all()


# TODO: fix the pre-selection of all outfits and all users currently in the system for the collaborators and outfits
class ShowroomAdmin(admin.ModelAdmin):
    model = Showroom
    # form = ShowroomAdminForm
    list_display = ('title', 'owner', 'is_public', 'date_created')
    list_filter = ('is_public', 'date_created')
    search_fields = ('title', 'owner__user__username')
    readonly_fields = ("date_created", "date_updated")
    ordering = ("-date_created",)

    # filter_horizontal = ('collaborators', 'outfits')


admin.site.register(Showroom, ShowroomAdmin)