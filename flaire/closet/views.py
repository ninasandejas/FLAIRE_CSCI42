import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import *
from .models import *


@login_required(login_url="user_management:login")
def closet(request):
    return render(request, "closet/outfit-builder.html", {"active_tab": "closet"})


def add_clothing_item(request):
    category = request.GET.get("category")

    if request.method == "POST":  # processes the form, binding user data
        form = AddClothingItemForm(request.POST, request.FILES)
        if form.is_valid():
            clothing_item = form.save(commit=False)
            clothing_item.owner = request.user.profile
            clothing_item.save()
            return redirect("closet:closet")
    else:  # displays/renders the form
        initial_data = {}
        if category:
            initial_data["category"] = category.upper()
        form = AddClothingItemForm(initial=initial_data)
    return render(
        request,
        "closet/add-clothing-item.html",
        {"form": form, "active_tab": "closet"},
    )


# for saving outfit
def save_outfit(request):
    if request.method == "POST":
        outfit_image = request.FILES.get("image")
        listed_item_ids = json.loads(
            request.POST.get("listed_item_ids", "[]")
        )  # get ids of items in the dropzone once the outfit collage is saved

        outfit = Outfit.objects.create(owner=request.user.profile, image=outfit_image)
        outfit.listed_items.clear()

        outfit.listed_items.set(ClothingItem.objects.filter(id__in=listed_item_ids))

        return JsonResponse({"success": True, "outfit_id": outfit.id})
    return JsonResponse({"success": False, "message": "Invalid request."}, status=400)


# for creating post
def save_outfit_post_metadata(request, outfit_id):
    outfit = get_object_or_404(Outfit, id=outfit_id, owner=request.user.profile)

    caption = request.POST.get(
        "caption", ""
    ).strip()  # remove leading and trailing whitespaces
    tags = request.POST.getlist("tags")[:3]  # limit to 3 tags per post

    outfit.caption = caption
    outfit.tags.set(tags)  # django-taggit accepts a list of strings
    outfit.save()

    return JsonResponse({"success": True})


def clothing_item_images(request):
    category = request.GET.get("category")
    items = ClothingItem.objects.filter(owner=request.user.profile)

    if category:
        items = items.filter(category=category.upper())

    image_data = [{"id": item.id, "url": item.image.url} for item in items]
    return JsonResponse({"images": image_data})
