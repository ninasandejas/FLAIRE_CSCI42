from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from user_management.models import Profile
from closet.models import ClothingItem, Comment, Outfit
from showrooms.models import Showroom
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
        showroom_data = [
            {
                "id": showroom.id,
                "url": showroom.cover_image.url if showroom.cover_image else "",
                "title": showroom.title
            }
            for showroom in showrooms
        ]
        return JsonResponse({"showrooms": showroom_data})


class FollowingOutfitsGridView(LoginRequiredMixin, View):
    def get(self, request):
        following_ids = Follow.objects.filter(follower=request.user.profile).values_list('following_id', flat=True)
        following_profiles = Profile.objects.filter(id__in=following_ids)
        outfits = Outfit.objects.filter(owner__in=following_profiles).order_by("-date_created")

        image_data = [{"id": outfit.id, "url": outfit.image.url if outfit.image else ""} for outfit in outfits]
        return JsonResponse({"images": image_data})


class FollowingShowroomsGridView(LoginRequiredMixin, View):
    def get(self, request):
        following_ids = Follow.objects.filter(follower=request.user.profile).values_list('following_id', flat=True)
        following_profiles = Profile.objects.filter(id__in=following_ids)
        showrooms = Showroom.objects.filter(owner__in=following_profiles).order_by("-date_created")

        showroom_data = [
            {
                "id": showroom.id,
                "url": showroom.cover_image.url if showroom.cover_image else "",
                "title": showroom.title
            }
            for showroom in showrooms
        ]
        return JsonResponse({"showrooms": showroom_data})


class OutfitDetailView(View):
    def get(self, request, pk):
        outfit = Outfit.objects.get(pk=pk)

        tags = (
            [tag.name for tag in outfit.tags.all()] if hasattr(outfit, "tags") else []
        )

        if hasattr(outfit, "comments"):
            comments = [
                {"author": comment.author.user.username, "entry": comment.entry}
                for comment in outfit.comments.all()
            ]
        else:
            comments = []

        listed_items = []
        if hasattr(outfit, "listed_items"):
            listed_items = [
                {
                    "id": item.id,
                    "url": item.image.url,
                    "name": item.name,
                    "brand": item.brand,
                    "owner": item.owner.user.username,
                }
                for item in outfit.listed_items.all()
            ]

        outfit_data = {
            "id": outfit.id,
            "url": outfit.image.url,
            "caption": outfit.caption or "",
            "tags": tags,
            "likes": outfit.likes.count() if hasattr(outfit, "likes") else 0,
            "comments": [
                {
                    "author": comment.author.user.username,
                    "entry": comment.entry,
                }
                for comment in outfit.comments.all()
            ],
            "listed_items": listed_items,
            "owner": (
                outfit.owner.user.username if hasattr(outfit, "owner") else "unknown"
            ),
        }

        return JsonResponse(outfit_data)


@method_decorator(csrf_exempt, name="dispatch")
class SubmitCommentView(View):
    def post(self, request, outfit_id):
        data = json.loads(request.body)
        entry = data.get("entry")
        outfit = Outfit.objects.get(id=outfit_id)
        comment = Comment.objects.create(
            outfit=outfit, author=request.user.profile, entry=entry
        )
        return JsonResponse(
            {"author": comment.author.user.username, "entry": comment.entry}
        )
