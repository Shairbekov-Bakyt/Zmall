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
    FavoriteAdvert,
    Comment,
    Help,
    HelpCategory,
    AdvertStatistics,
    AdvertReport
)

admin.site.register(City)
admin.site.register(SubCategory)
admin.site.register(FavoriteAdvert)
admin.site.register(Help)
admin.site.register(HelpCategory)
admin.site.register(Comment)


class AdvertImageInline(admin.TabularInline):
    model = AdvertImage
    max_num = 8


class AdvertContactInline(admin.TabularInline):
    model = AdvertContact
    max_num = 8


class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ("user", "text", "parent")


class AdvertStatisticsInline(admin.StackedInline):
    model = AdvertStatistics
    readonly_fields = ("advert_contacts_view", "advert_views", "date")


class AdvertReportInline(admin.StackedInline):
    model = AdvertReport
    readonly_fields = ("report_message", "report")


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    inlines = [AdvertImageInline, AdvertContactInline,
               CommentInline, AdvertReportInline,
               AdvertStatisticsInline]

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
