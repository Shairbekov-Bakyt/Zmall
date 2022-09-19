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
    Comment,
    Help,
    HelpCategory,
    AdvertStatistics,
    AdvertReport,
    Feedback,
    FeedbackMessage,
    PrivacyPolicy,
)

admin.site.register(City)
admin.site.register(Feedback)
admin.site.register(Comment)


class AdvertImageInline(admin.TabularInline):
    model = AdvertImage
    max_num = 8


class AdvertContactInline(admin.TabularInline):
    model = AdvertContact
    max_num = 8


class CommentInline(admin.StackedInline):
    model = Comment
    readonly_fields = ("user", "text", "parent")


class AdvertStatisticsInline(admin.StackedInline):
    model = AdvertStatistics


class AdvertReportInline(admin.StackedInline):
    model = AdvertReport
    readonly_fields = ["report_message", "report"]

    # def get_readonly_fields(self, request, obj=None):
    #     if self.get_queryset(request).last().report_message is None:
    #         return ['report', ]
    #
    #     return ['report_message', ]

    def get_empty_value_display(self):
        return "empty"


class HelpInline(admin.StackedInline):
    model = Help
    readonly_fields = ("view",)


class SubCategoryInline(admin.StackedInline):
    model = SubCategory


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    inlines = [
        AdvertImageInline,
        AdvertContactInline,
        CommentInline,
        AdvertReportInline,
        AdvertStatisticsInline,
    ]

    class Meta:
        model = Advert


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]

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
    def has_add_permission(self, request):
        has_add = super().has_add_permission(request)
        if has_add and Promote.objects.count() >= 3:
            has_add = False
        return has_add

    class Meta:
        model = Promote


@admin.register(HelpCategory)
class HelpCategoryAdmin(admin.ModelAdmin):
    inlines = [HelpInline]

    class Meta:
        model = HelpCategory


@admin.register(FeedbackMessage)
class FeedbackMessageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        has_add = super().has_add_permission(request)
        if has_add and FeedbackMessage.objects.exists():
            has_add = False
        return has_add

    class Meta:
        model = FeedbackMessage


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        has_add = super().has_add_permission(request)
        if has_add and PrivacyPolicy.objects.exists():
            has_add = False
        return has_add

    class Meta:
        model = PrivacyPolicy
