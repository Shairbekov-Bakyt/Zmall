from django.contrib import admin

from advert.models import (
    Advert,
    AdvertContact,
    AdvertImage,
    Category,
    City,
    Promote,
    SubCategory,
)

admin.site.register(Advert)
admin.site.register(AdvertImage)
admin.site.register(AdvertContact)
admin.site.register(Category)
admin.site.register(City)
admin.site.register(Promote)
admin.site.register(SubCategory)
