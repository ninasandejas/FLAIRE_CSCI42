from django.contrib import admin

from .models import Follow, Notification

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__user__username', 'following__user__username')
    
@admin.register(Notification)
class NotifAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('recipient', 'message', 'created_at', 'is_read')
    list_filter = ('recipient', 'is_read')
    search_fields = ('recipient__profile__user', 'message')
    ordering = ('recipient', '-created_at')