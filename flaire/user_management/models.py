from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model
from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfileManager:
    @staticmethod
    def get_profile(user):
        return Profile.objects.get(user=user)

    @staticmethod
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()

# Add the profile property to the User model
User.add_to_class('profile', property(UserProfileManager.get_profile))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_address = models.EmailField()
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Stores profile images
    ootd = models.OneToOneField("closet.Outfit", on_delete=models.SET_NULL, null=True, blank=True, related_name="ootd_profile")

    followers = models.ManyToManyField(
        User, symmetrical=False, related_name="following", blank=True
    )

    def __str__(self):
        return self.user.username

      
# class ProfileFollower(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     date_followed = models.DateTimeField(auto_now_add=True)

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(
        "closet.ClothingItem", on_delete=models.CASCADE)
