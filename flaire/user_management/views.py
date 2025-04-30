import logging

from closet.models import ClothingItem, Outfit
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.shortcuts import render, redirect

from .forms import LoginForm, ProfileSetupForm, SignUpForm, ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from showrooms.models import Showroom
from django.db.models import Q, Count

logger = logging.getLogger(__name__)

# class UserUpdateView(LoginRequiredMixin, UpdateView):
#     model = Profile
#     form_class = ProfileForm
#     template_name = 'user_detail.html'
#     success_url = reverse_lazy('homepage:homepage')

#     def get_object(self, queryset=None):
#         return self.request.user.profile

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


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

        Profile.objects.create(user=user, email_address=user.email)

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


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('user_management:login')

        profile, created = Profile.objects.get_or_create(user=request.user)
        clothing_items = ClothingItem.objects.filter(owner=profile) if profile else []
        showrooms = Showroom.objects.filter(
            Q(owner=profile) |
            Q(showroomcollaborator__collaborator=profile, showroomcollaborator__status='ACCEPTED')
        ).annotate(follower_count=Count('followers')).order_by('-follower_count').distinct()[:3]

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
        showrooms = Showroom.objects.filter(
            Q(owner=profile) |
            Q(showroomcollaborator__collaborator=profile, showroomcollaborator__status='ACCEPTED')
        ).annotate(follower_count=Count('followers')).order_by('-follower_count').distinct()[:3]

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
        try:
            user = User.objects.get(username=username)
            profile = user.profile
        except User.DoesNotExist:
            return redirect("user_management:profile")

        clothing_items = ClothingItem.objects.filter(owner=profile) if profile else []
        showrooms = Showroom.objects.filter(
            Q(owner=profile) |
            Q(showroomcollaborator__collaborator=profile, showroomcollaborator__status='ACCEPTED')
        ).annotate(follower_count=Count('followers')).order_by('-follower_count').distinct()[:3]

        is_following = request.user.following.filter(id=profile.user.id).exists()

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

        user_profile = request.user

        if profile.user in user_profile.following.all():
            user_profile.following.remove(profile.user)
        else:
            user_profile.following.add(profile.user)

        return redirect("user_management:other_user_profile", username=username)
