from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from user_management.models import Profile
from closet.models import ClothingItem, Comment, Outfit
from showrooms.models import Showroom, ShowroomFollower, ShowroomCollaborator
from .models import Follow
import json


@login_required
def explore(request):
    return render(request, "social/explore.html", {
        "active_tab": "explore"
    })

@login_required
def following(request):
    return render(request, "social/following.html", {
        "active_tab": "following"
    })


class ExploreOutfitsGridView(LoginRequiredMixin, View):
    def get(self, request):
        outfits = Outfit.objects.all().order_by("-date_created")

        image_data = [{"id": outfit.id, "url": outfit.image.url if outfit.image else ""} for outfit in outfits]
        return JsonResponse({"images": image_data})

class ExploreShowroomsGridView(LoginRequiredMixin, View):
    def get(self, request):
        showrooms = Showroom.objects.all().order_by("-date_updated")
        image_data = [
            {
                "id": showroom.id,
                "slug": showroom.slug,
                "title": showroom.title,
                "cover_image": showroom.cover_image.url if showroom.cover_image else "",
            }
        for showroom in showrooms
        ]
        return JsonResponse({"images": image_data})


class FollowingOutfitsGridView(LoginRequiredMixin, View):
    def get(self, request):
        following_ids = Follow.objects.filter(follower=request.user.profile).values_list('following_id', flat=True)
        following_profiles = Profile.objects.filter(id__in=following_ids)
        outfits = Outfit.objects.filter(owner__in=following_profiles).order_by("-date_created")

        image_data = [{"id": outfit.id, "url": outfit.image.url if outfit.image else ""} for outfit in outfits]
        return JsonResponse({"images": image_data})


class FollowingShowroomsGridView(LoginRequiredMixin, View):
    def get(self, request):
        following_showrooms = ShowroomFollower.objects.filter(profile=request.user.profile)
        following_showroom_ids = following_showrooms.values_list('showroom_id', flat=True)
        collaborator_showrooms = ShowroomCollaborator.objects.filter(collaborator=request.user.profile)
        collaborator_showroom_ids = collaborator_showrooms.values_list('showroom_id', flat=True)
        showroom_ids = following_showroom_ids.union(collaborator_showroom_ids)
        showrooms = Showroom.objects.filter(id__in=showroom_ids).order_by("-date_updated")
        image_data = [
            {
                "id": showroom.id,
                "slug": showroom.slug,
                "title": showroom.title,
                "cover_image": showroom.cover_image.url if showroom.cover_image else "",
            }
        for showroom in showrooms
        ]
        return JsonResponse({"images": image_data})
