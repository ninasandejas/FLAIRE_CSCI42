import json
import logging

from closet.models import ClosetItem, ClothingItem, Comment, Outfit
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, FormView, UpdateView
from showrooms.models import Showroom
from social.models import Notification

from .forms import LoginForm, ProfileForm, ProfileSetupForm, SignUpForm
from .models import LikedOutfit, Profile, WishlistItem

logger = logging.getLogger(__name__)


class UserLoginView(FormView):
    model = User
    template_name = "user_management/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("user_management:profile")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "next" in self.request.GET:
            context["warning_message"] = (
                "*you need to be logged in to access this page."
            )
        return context


class UserCreateView(CreateView):
    model = Profile
    form_class = SignUpForm
    template_name = "user_management/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("user_management:profile"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()

        Profile.objects.get_or_create(user=user, defaults={"email_address": user.email})

        login(self.request, user)

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("user_management:profile_setup")


class ProfileSetupView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileSetupForm
    template_name = "user_management/profile_setup.html"
    success_url = reverse_lazy("user_management:profile")

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        bio = form.cleaned_data.get("bio", "").strip()
        profile_picture = form.cleaned_data.get("profile_picture")

        if not bio and not profile_picture:
            form.add_error(None, "please provide at least a bio or a profile picture.")
            return self.form_invalid(form)

        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("user_management:login")

        profile, created = Profile.objects.get_or_create(user=request.user)
        wishlist_items = WishlistItem.objects.filter(user=request.user).select_related(
            "item"
        )
        clothing_items = [w.item for w in wishlist_items] if profile else []
        showrooms = (
            Showroom.objects.filter(
                Q(owner=profile)
                | Q(
                    showroomcollaborator__collaborator=profile,
                    showroomcollaborator__status="ACCEPTED",
                )
            )
            .annotate(follower_count=Count("followers"))
            .order_by("-follower_count")
            .distinct()[:3]
        )

        form = ProfileForm(instance=profile)

        return render(
            request,
            "user_management/profile.html",
            {
                "profile": profile,
                "items": clothing_items,
                "showrooms": showrooms,
                "form": form,
                "active_tab": "profile",
                "is_own_profile": True,
            },
        )

    def post(self, request):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_management:profile")

        wishlist_items = WishlistItem.objects.filter(user=request.user).select_related(
            "item"
        )
        clothing_items = [w.item for w in wishlist_items] if profile else []
        showrooms = (
            Showroom.objects.filter(
                Q(owner=profile)
                | Q(
                    showroomcollaborator__collaborator=profile,
                    showroomcollaborator__status="ACCEPTED",
                )
            )
            .annotate(follower_count=Count("followers"))
            .order_by("-follower_count")
            .distinct()[:3]
        )

        return render(
            request,
            "user_management/profile.html",
            {
                "profile": profile,
                "items": clothing_items,
                "showrooms": showrooms,
                "form": form,
                "active_tab": "profile",
            },
        )


class LikedOutfitsView(LoginRequiredMixin, View):
    def get(self, request):
        liked_outfit_ids = LikedOutfit.objects.filter(user=request.user).values_list(
            "outfit_id", flat=True
        )
        outfits = Outfit.objects.filter(id__in=liked_outfit_ids).prefetch_related(
            "listed_items"
        )
        return render(
            request,
            "user_management/liked_outfits.html",
            {
                "outfits": outfits,
                "active_tab": "liked_outfits",
            },
        )


class WishlistView(LoginRequiredMixin, View):
    def get(self, request):
        wishlist_items = WishlistItem.objects.filter(user=request.user).select_related(
            "item"
        )
        return render(
            request,
            "user_management/wishlist.html",
            {
                "items": [w.item for w in wishlist_items],
                "active_tab": "wishlist",
            },
        )


class OtherUserProfileView(View):
    def get(self, request, username):
        # check if the username matches the logged-in user's username
        if username == request.user.username:
            return redirect("user_management:profile")

        try:
            user = User.objects.get(username=username)
            profile = user.profile
        except User.DoesNotExist:
            return redirect("user_management:profile")

        outfits = Outfit.objects.filter(owner=profile).order_by("-date_created")

        wishlist_items = WishlistItem.objects.filter(user=profile.user).select_related("item")
        clothing_items = [w.item for w in wishlist_items] if profile else []
        showrooms = (
            Showroom.objects.filter(
                Q(owner=profile)
                | Q(
                    showroomcollaborator__collaborator=profile,
                    showroomcollaborator__status="ACCEPTED",
                )
            )
            .annotate(follower_count=Count("followers"))
            .order_by("-follower_count")
            .distinct()[:3]
        )

        is_following = profile.followers.filter(id=request.user.id).exists()

        return render(
            request,
            "user_management/profile.html",
            {
                "profile": profile,
                "items": clothing_items,
                "outfits": outfits,
                "showrooms": showrooms,
                "is_following": is_following,
                "is_own_profile": False,
                "active_tab": "profile",
            },
        )

    def post(self, request, username):
        try:
            user = User.objects.get(username=username)
            profile = user.profile
        except User.DoesNotExist:
            return redirect("user_management:profile")

        # Prevent users from following themselves
        if user == request.user:
            return redirect("user_management:other_user_profile", username=username)

        # Correct the follow/unfollow logic
        if profile.followers.filter(id=request.user.id).exists():
            profile.followers.remove(request.user)
        else:
            profile.followers.add(request.user)
            user_to_follow = User.objects.get(username=username)
            # creating notification for every follow from a user
            Notification.objects.create(
                sender=request.user.profile,
                recipient=user_to_follow.profile,
                message=f"{request.user.username} followed you.",
                link=reverse(
                    "user_management:other_user_profile",
                    kwargs={"username": request.user.username},
                ),
                is_read=False,
            )

        return redirect("user_management:other_user_profile", username=username)


class UserFollowView(View):
    @method_decorator(login_required)
    def get_followers(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)
        followers = profile.followers.all()
        followers_data = [
            {
                "username": follower.username,
                "profile_picture_url": (
                    follower.profile.profile_picture.url
                    if follower.profile.profile_picture
                    else ""
                ),
                "follow_status": (
                    "Unfollow"
                    if follower.profile.followers.filter(id=request.user.id).exists()
                    else "Follow"
                ),
            }
            for follower in followers
        ]
        if not followers_data:
            return JsonResponse([], safe=False)
        return JsonResponse(followers_data, safe=False)

    @method_decorator(login_required)
    def get_following(self, request, username):
        user = get_object_or_404(User, username=username)
        try:
            following_profiles = Profile.objects.filter(followers=user)
            following_data = [
                {
                    "username": profile.user.username,
                    "profile_picture_url": (
                        profile.profile_picture.url if profile.profile_picture else ""
                    ),
                    "follow_status": (
                        "Unfollow"
                        if profile.followers.filter(id=request.user.id).exists()
                        else "Follow"
                    ),
                }
                for profile in following_profiles
            ]
            if not following_data:
                return JsonResponse([], safe=False)
            return JsonResponse(following_data, safe=False)
        except Exception as e:
            logger.error(f"Error in get_following: {e}")
            return JsonResponse(
                {"error": "An error occurred while fetching following data."},
                status=500,
            )

    @method_decorator(login_required)
    def toggle_follow(self, request, username):
        try:
            user_to_follow = get_object_or_404(User, username=username)
            profile_to_follow = user_to_follow.profile

            if profile_to_follow.followers.filter(id=request.user.id).exists():
                profile_to_follow.followers.remove(request.user)
                new_status = "Follow"
            else:
                profile_to_follow.followers.add(request.user)
                new_status = "Unfollow"

            return JsonResponse({"new_status": new_status})
        except Exception as e:
            logger.error(f"Error in toggle_follow: {e}")
            return JsonResponse(
                {"error": "An error occurred while toggling follow status."}, status=500
            )


class OutfitGridImagesView(View):
    def get(self, request, username=None):
        if username:
            user = get_object_or_404(User, username=username)
            profile = user.profile
        else:
            profile = request.user.profile

        outfits = Outfit.objects.filter(owner=profile).order_by("-date_created")

        image_data = [{"id": outfit.id, "url": outfit.image.url} for outfit in outfits]
        return JsonResponse({"images": image_data})


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
                    "is_in_closet": ClosetItem.objects.filter(
                        closet_owner=request.user.profile, clothing_item=item
                    ).exists(),
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


@csrf_exempt
@require_POST
def toggle_wishlist(request, item_id):
    try:
        item = ClothingItem.objects.get(id=item_id)
        wishlist_item, created = WishlistItem.objects.get_or_create(
            user=request.user, item=item
        )
        if not created:
            wishlist_item.delete()
            return JsonResponse({"status": "removed"})
        return JsonResponse({"status": "added"})
    except ClothingItem.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Item not found"}, status=404
        )


@csrf_exempt
@require_POST
def toggle_like_outfit(request, outfit_id):
    try:
        outfit = Outfit.objects.get(id=outfit_id)
        liked, created = LikedOutfit.objects.get_or_create(
            user=request.user, outfit=outfit
        )
        if not created:
            liked.delete()
            return JsonResponse({"status": "unliked"})
        return JsonResponse({"status": "liked"})
    except Outfit.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Outfit not found"}, status=404
        )


@csrf_exempt
def remove_from_wishlist(request, item_id):
    if request.method == "POST":
        try:
            item = ClothingItem.objects.get(id=item_id)
            item.liked_by.remove(request.user.profile)
            return JsonResponse({"status": "removed"})
        except ClothingItem.DoesNotExist:
            return JsonResponse({"status": "not_found"}, status=404)

    return JsonResponse({"status": "invalid_method"}, status=405)


@csrf_exempt
def unlike_outfit(request, outfit_id):
    if request.method == "POST":
        LikedOutfit.objects.filter(user=request.user, outfit_id=outfit_id).delete()
        return JsonResponse({"status": "unliked"})
    return JsonResponse({"status": "error"}, status=400)


@require_POST
def add_to_closet(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id)
    obj, created = ClosetItem.objects.get_or_create(
        closet_owner=request.user.profile, clothing_item=item
    )
    return JsonResponse({"status": "added" if created else "already_in_closet"})
