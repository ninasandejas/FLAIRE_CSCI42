from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import *
from .models import *


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


def clothing_item_images(request):
    category = request.GET.get("category")
    items = ClothingItem.objects.all()

    if category:
        items = items.filter(category=category.upper())

    image_urls = [item.image.url for item in items]
    return JsonResponse({"images": image_urls})
