from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInLine(admin.StackedInline):
    model = Profile 
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInLine,]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)