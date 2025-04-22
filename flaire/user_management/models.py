from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model
from django.apps import apps



# will fix following/followers issue later
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_address = models.EmailField()
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Stores profile images

    followers = models.ManyToManyField(User, symmetrical=False, related_name="following", blank=True)

    def __str__(self):
        return self.user.username
    


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(
        "closet.ClothingItem", on_delete=models.CASCADE)  

   