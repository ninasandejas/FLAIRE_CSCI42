from django.contrib import admin

from .models import ClosetItem, ClothingItem, Comment, Outfit


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
    list_filter = ("owner", "category", "color", "brand")
    search_fields = (
        "brand",
        "owner__user__username",
    )
    readonly_fields = ("date_created", "date_updated")
    ordering = ("-date_created",)


class ClosetItemAdmin(admin.ModelAdmin):
    list_display = ("id", "closet_owner", "clothing_item", "date_added")
    list_filter = ("closet_owner",)
    search_fields = ("closet_owner__user__username", "clothing_item__name")
    readonly_fields = ("date_added",)
    ordering = ("-date_added",)


class OutfitAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "caption", "date_created", "date_updated")
    list_filter = ("date_created",)
    search_fields = ("owner__user__username",)
    readonly_fields = (
        "listed_items",
        "likes",
        "date_created",
        "date_updated",
    )
    ordering = ("-date_created",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "outfit", "author", "entry", "date_created", "date_updated")
    readonly_fields = ("outfit", "date_created", "date_updated")


admin.site.register(ClothingItem, ClothingItemAdmin)
admin.site.register(ClosetItem, ClosetItemAdmin)
admin.site.register(Outfit, OutfitAdmin)
admin.site.register(Comment, CommentAdmin)
