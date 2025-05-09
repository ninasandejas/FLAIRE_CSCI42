from django.contrib import admin
from .models import *

@admin.register(Notification)
class NotifAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('recipient', 'message', 'created_at', 'is_read')
    list_filter = ('recipient', 'is_read')
    search_fields = ('recipient__profile__user', 'message')
    ordering = ('recipient', '-created_at')