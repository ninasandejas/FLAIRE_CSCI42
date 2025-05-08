import json

from closet.models import ClothingItem, Comment, Outfit
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, FormView, UpdateView
from .models import WishlistItem 
from django.views.decorators.http import require_POST
from .models import LikedOutfit
from closet.models import Outfit
from django.contrib.auth.decorators import login_required




from .forms import LoginForm, ProfileSetupForm, SignUpForm
from .models import Profile

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


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return render(
            request,
            "user_management/profile.html",
            {"profile": profile, "active_tab": "profile"},
        )


class LikedOutfitsView(LoginRequiredMixin, View):
    def get(self, request):
        liked_outfit_ids = LikedOutfit.objects.filter(user=request.user).values_list("outfit_id", flat=True)
        outfits = Outfit.objects.filter(id__in=liked_outfit_ids).prefetch_related("listed_items")
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
        wishlist_items = WishlistItem.objects.filter(user=request.user).select_related("item")
        return render(
            request,
            "user_management/wishlist.html",
            {
                "items": [w.item for w in wishlist_items],  
                "active_tab": "wishlist",
            },
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

@csrf_exempt
@require_POST
def toggle_wishlist(request, item_id):
    try:
        item = ClothingItem.objects.get(id=item_id)
        wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, item=item)
        if not created:
            wishlist_item.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})
    except ClothingItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
    

@csrf_exempt
@require_POST
def toggle_like_outfit(request, outfit_id):
    try:
        outfit = Outfit.objects.get(id=outfit_id)
        liked, created = LikedOutfit.objects.get_or_create(user=request.user, outfit=outfit)
        if not created:
            liked.delete()
            return JsonResponse({'status': 'unliked'})
        return JsonResponse({'status': 'liked'})
    except Outfit.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Outfit not found'}, status=404)
    
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