from django.db import models
from user_management.models import Profile

class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="following_relations")
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_relations")
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='send_notifications')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receive_notifications')
    message = models.CharField(max_length=255)
    link = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.recipient.user}: {self.message[:20]}..."