from django.contrib import admin

from user.models import CustomUser
from advert.models import FavoriteAdvert


class FavoriteAdvertInline(admin.StackedInline):
    model = FavoriteAdvert


@admin.register(CustomUser)
class AdvertAdmin(admin.ModelAdmin):
    inlines = [FavoriteAdvertInline]

    class Meta:
        model = CustomUser
