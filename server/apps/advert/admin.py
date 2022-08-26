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
)

admin.site.register(City)


class AdvertImageInline(admin.TabularInline):
    model = AdvertImage
    max_num = 8


class AdvertContactInline(admin.TabularInline):
    model = AdvertContact
    max_num = 8


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    inlines = [AdvertImageInline, AdvertContactInline]

    def img_tag(self, obj):
        return format_html(
            '<img src="{url}" width="{width}" height={height}/>'.format(
                url=obj.advert_image.url, width=150, height=150
            )
        )

    img_tag.short_description = "Image"

    readonly_fields = [
        "img_tag",
    ]

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

    readonly_fields = ["img_tag", "advert_count"]

    class Meta:
        model = Category


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):

    readonly_fields = ["advert_count"]

    class Meta:
        model = SubCategory


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
