from django.contrib import admin

from .models import ClothingItem, Comment, Outfit


class ClothingItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uploader",
        "name",
        "category",
        "brand",
        "color",
        "image",
    )
    list_filter = ("uploader", "category", "color", "brand")
    search_fields = (
        "brand",
        "uploader__user__username",
    )
    readonly_fields = ("date_created", "date_updated")
    ordering = ("-date_created",)


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
admin.site.register(Outfit, OutfitAdmin)
admin.site.register(Comment, CommentAdmin)
