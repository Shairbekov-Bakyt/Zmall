from django.contrib import admin
from django.utils.html import format_html

from advert.models import (
    Advert,
    AdvertContact,
    AdvertImage,
    Category,
    City,
    Promote,
    SubCategory,
    AdvertView,
    FavoriteAdvert,
)

admin.site.register(City)
admin.site.register(SubCategory)
admin.site.register(FavoriteAdvert)


class AdvertImageInline(admin.TabularInline):
    model = AdvertImage
    max_num = 8


class AdvertContactInline(admin.TabularInline):
    model = AdvertContact
    max_num = 8


class AdvertViewInline(admin.StackedInline):
    model = AdvertView
    readonly_fields = ("users", "view")


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    inlines = [AdvertImageInline, AdvertContactInline, AdvertViewInline]

    class Meta:
        model = Advert


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def img_tag(self, obj):
        return format_html(
            '<img src="{url}" width="{width}" height={height}/>'.format(
                url=obj.icon.url, width=150, height=150
            )
        )

    img_tag.short_description = "Image"

    readonly_fields = ["img_tag"]

    class Meta:
        model = Category


@admin.register(Promote)
class PromoteAdmin(admin.ModelAdmin):
    def img_tag(self, obj):
        return format_html(
            '<img src="{url}" width="{width}" height={height}/>'.format(
                url=obj.icon.url, width=150, height=150
            )
        )

    img_tag.short_description = "Image"

    readonly_fields = ["img_tag"]

    class Meta:
        model = Promote
