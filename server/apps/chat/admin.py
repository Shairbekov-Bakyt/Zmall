from django.contrib import admin
from .models import Chat, Room


class ChatInline(admin.StackedInline):
    model = Chat


@admin.register(Room)
class AdvertAdmin(admin.ModelAdmin):
    inlines = [ChatInline]

    class Meta:
        model = Room
