from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from user_management.models import Profile
from closet.models import Outfit
from showrooms.models import Showroom
from .models import Follow


@login_required
def explore(request):
    following_ids = Follow.objects.filter(follower=request.user.profile).values_list('following_id', flat=True)
    explore_profiles = Profile.objects.exclude(id__in=following_ids).exclude(id=request.user.profile.id)

    outfits = Outfit.objects.filter(owner__in=explore_profiles)
    showrooms = Showroom.objects.filter(owner__in=explore_profiles)

    return render(request, "social/explore.html", {
        "outfits": outfits,
        "showrooms": showrooms,
        "active_tab": "explore"
    })


@login_required
def following(request):
    following_ids = Follow.objects.filter(follower=request.user.profile).values_list('following_id', flat=True)
    following_profiles = Profile.objects.filter(id__in=following_ids)

    outfits = Outfit.objects.filter(owner__in=following_profiles)
    showrooms = Showroom.objects.filter(owner__in=following_profiles)

    return render(request, "social/following.html", {
        "outfits": outfits,
        "showrooms": showrooms,
        "active_tab": "following"
    })


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