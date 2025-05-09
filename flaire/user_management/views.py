import json
import logging

from closet.models import ClothingItem, Comment, Outfit
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, FormView, UpdateView
from showrooms.models import Showroom

from .forms import LoginForm, ProfileForm, ProfileSetupForm, SignUpForm
from .models import Profile

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
        clothing_items = ClothingItem.objects.filter(owner=profile) if profile else []
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

        clothing_items = ClothingItem.objects.filter(owner=profile) if profile else []
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


class LikedOutfitsView(View):
    def get(self, request):
        outfits = Outfit.objects.filter(owner=request.user.profile).prefetch_related(
            "items"
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
        user_profile = request.user.profile
        clothing_items = ClothingItem.objects.filter(owner=user_profile)
        return render(
            request,
            "user_management/wishlist.html",
            {
                "items": clothing_items,
                "active_tab": "wishlist",
            },
        )


class OtherUserProfileView(View):
    def get(self, request, username):
        # Check if the username matches the logged-in user's username
        if username == request.user.username:
            return redirect("user_management:profile")

        try:
            user = User.objects.get(username=username)
            profile = user.profile
        except User.DoesNotExist:
            return redirect("user_management:profile")

        clothing_items = ClothingItem.objects.filter(owner=profile) if profile else []
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
    def get(self, request):
        outfits = Outfit.objects.filter(owner=request.user.profile).order_by(
            "-date_created"
        )
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
