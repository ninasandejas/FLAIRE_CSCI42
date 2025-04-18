from django.contrib import admin

from .models import ClothingItem, Outfit


class ClothingItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "name",
        "category",
        "brand",
        "color",
        "image",
    )
    list_filter = ("category", "color", "brand")
    search_fields = (
        "brand",
        "owner__user__username",
    )
    readonly_fields = ("date_created", "date_updated")
    ordering = ("-date_created",)


class OutfitAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "date_created", "date_updated")
    list_filter = ("date_created",)
    search_fields = ("owner__user__username",)
    readonly_fields = ("date_created", "date_updated")
    ordering = ("-date_created",)


admin.site.register(ClothingItem, ClothingItemAdmin)
admin.site.register(Outfit, OutfitAdmin)
