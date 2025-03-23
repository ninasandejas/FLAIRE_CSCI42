from django.http import JsonResponse
from django.shortcuts import render

from .models import *


def closet(request):
    return render(request, "closet/outfit-builder.html", {"active_tab": "closet"})


def add_clothing_item(request):
    return render(request, "closet/add-clothing-item.html", {"active_tab": "closet"})


def clothing_item_images(request):
    category = request.GET.get("category")
    items = ClothingItem.objects.all()

    if category:
        items = items.filter(category=category.upper())

    image_urls = [item.image.url for item in items]
    return JsonResponse({"images": image_urls})
