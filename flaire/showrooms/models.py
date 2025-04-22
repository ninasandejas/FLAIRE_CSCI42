from django.db import models
from user_management.models import Profile
from closet.models import Outfit
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager
from django.utils import timezone


class Showroom(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="owned_showrooms", null=True
    )
    cover_image = models.ImageField(upload_to="showroomimages/", blank=True, null=True)
    is_public = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)

    collaborators = models.ManyToManyField(
        Profile,
        through='ShowroomCollaborator',
        through_fields=('showroom', 'collaborator'),
        related_name="collaborated_showrooms", 
        blank=True
    )

    outfits = models.ManyToManyField(
        Outfit,
        through='ShowroomOutfit',
        related_name='included_in_showrooms'
    )
    
    followers  = models.ManyToManyField(
        Profile,
        through='ShowroomFollower',
        related_name='followed_showrooms'
        )

    def __str__(self):
        return self.title
    


class ShowroomOutfit(models.Model):
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    # notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('showroom', 'outfit')

    def __str__(self):
        return f"{self.outfit} in {self.showroom}"


class ShowroomFollower(models.Model):
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_followed = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('showroom', 'profile')

    def clean(self):
        if self.profile == self.showroom.owner:
            raise ValidationError("The owner cannot follow their own showroom.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.profile} follows {self.showroom}"


class ShowroomCollaborator(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    collaborator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='sent_collab_invites')
    date_invited = models.DateTimeField(auto_now_add=True)
    date_accepted = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        unique_together = ('showroom', 'collaborator')

    def save(self, *args, **kwargs):
        if self.status == 'ACCEPTED' and self.date_accepted is None:
            self.date_accepted = timezone.now()
        elif self.status != 'ACCEPTED':
            self.date_accepted = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.collaborator} in {self.showroom} ({self.status})"