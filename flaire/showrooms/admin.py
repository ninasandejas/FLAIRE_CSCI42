from django import forms
from django.contrib import admin

from .models import *


class ShowroomCollaboratorInline(admin.TabularInline):
    model = ShowroomCollaborator
    extra = 1
    # autocomplete_fields = ['outfit']


class ShowroomOutfitInline(admin.TabularInline):
    model = ShowroomOutfit
    extra = 1
    # autocomplete_fields = ['outfit']


class ShowroomFollowerInline(admin.TabularInline):
    model = ShowroomFollower
    extra = 1
    # autocomplete_fields = ['outfit']


class ShowroomAdmin(admin.ModelAdmin):
    model = Showroom
    list_display = ('title', 'owner', 'is_public', 'date_created')
    list_filter = ('is_public', 'date_created')
    search_fields = ('title', 'owner__user__username')
    readonly_fields = ("date_created", "date_updated")
    inlines = [ShowroomCollaboratorInline, ShowroomOutfitInline, ShowroomFollowerInline]
    ordering = ("-date_created",)

    # filter_horizontal = ('collaborators', 'outfits')


admin.site.register(Showroom, ShowroomAdmin)