from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
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
        search = request.GET.get('search', '').strip().lower()
        outfits = Outfit.objects.all().order_by("-date_created")

        if search:
            outfits = outfits.filter(
                Q(caption__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()

        image_data = [
            {
                "id": outfit.id,
                "url": outfit.image.url if outfit.image else "",
                "tags": [tag.name for tag in outfit.tags.all()]
            }
            for outfit in outfits
        ]
        return JsonResponse({"images": image_data})


class ExploreShowroomsGridView(LoginRequiredMixin, View):
    def get(self, request):
        search = request.GET.get('search', '').strip().lower()
        showrooms = Showroom.objects.all().order_by("-date_updated")

        if search:
            showrooms = showrooms.filter(
                Q(title__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()

        image_data = [
            {
                "id": showroom.id,
                "slug": showroom.slug,
                "title": showroom.title,
                "cover_image": showroom.cover_image.url if showroom.cover_image else "",
                "tags": [tag.name for tag in showroom.tags.all()]
            }
            for showroom in showrooms
        ]
        return JsonResponse({"images": image_data})


class FollowingOutfitsGridView(LoginRequiredMixin, View):
    def get(self, request):
        search = request.GET.get('search', '').strip().lower()
        following_ids = Follow.objects.filter(follower=request.user.profile).values_list('following_id', flat=True)
        following_profiles = Profile.objects.filter(id__in=following_ids)
        outfits = Outfit.objects.filter(owner__in=following_profiles).order_by("-date_created")

        if search:
            outfits = outfits.filter(
                Q(caption__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()

        image_data = [
            {
                "id": outfit.id,
                "url": outfit.image.url if outfit.image else "",
                "tags": [tag.name for tag in outfit.tags.all()]
            }
            for outfit in outfits
        ]
        return JsonResponse({"images": image_data})


class FollowingShowroomsGridView(LoginRequiredMixin, View):
    def get(self, request):
        search = request.GET.get('search', '').strip().lower()
        following_showrooms = ShowroomFollower.objects.filter(profile=request.user.profile)
        following_showroom_ids = following_showrooms.values_list('showroom_id', flat=True)
        collaborator_showrooms = ShowroomCollaborator.objects.filter(collaborator=request.user.profile)
        collaborator_showroom_ids = collaborator_showrooms.values_list('showroom_id', flat=True)
        showroom_ids = following_showroom_ids.union(collaborator_showroom_ids)
        showrooms = Showroom.objects.filter(id__in=showroom_ids).order_by("-date_updated")

        if search:
            showrooms = showrooms.filter(
                Q(title__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()
        
        image_data = [
            {
                "id": showroom.id,
                "slug": showroom.slug,
                "title": showroom.title,
                "cover_image": showroom.cover_image.url if showroom.cover_image else "",
                "tags": [tag.name for tag in showroom.tags.all()]
            }
            for showroom in showrooms
        ]
        return JsonResponse({"images": image_data})
  
@login_required
def fetch_notifications(request):
    notifications = request.user.profile.receive_notifications.order_by('-created_at')[:10]
    data = [{
        'message': n.message,
        'link': n.link,
        'created_at': n.created_at.strftime('%Y-%m-%d %H:%M'),
        'is_read': n.is_read,
    } for n in notifications]
    return JsonResponse({'notifications': data})


def display_explore(request):
    return
