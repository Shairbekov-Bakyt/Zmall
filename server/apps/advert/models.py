from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from config.settings.base import REDIS_HOST, REDIS_PORT
from user.models import CustomUser
from advert.utils import connect


class Category(models.Model):
    icon = models.ImageField(
        upload_to="category/icon/%Y/%m/%d", verbose_name="изображение категории"
    )
    name = models.CharField(max_length=100, verbose_name="название категории")
    advert_count = models.IntegerField(verbose_name="количество объявлении", default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def set_advert_count(cls, number):
        cls.advert_count = number
        cls.save()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )
    name = models.CharField(max_length=100, verbose_name="название подкатегори")
    advert_count = models.IntegerField(verbose_name="количество объявлении", default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def set_advert_count(cls, number):
        cls.advert_count = number
        cls.save()

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class AdvertImage(models.Model):
    advert_id = models.ForeignKey(
        "Advert",
        on_delete=models.CASCADE,
        verbose_name="объявления",
        related_name="advert_image",
    )
    image = models.ImageField(upload_to="advert/images/%Y/%m/%d")

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = "изображение для объявлении"
        verbose_name_plural = "изображении для объявлении"


class City(models.Model):
    name = models.CharField(max_length=150, verbose_name="название города")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class AdvertContact(models.Model):
    advert = models.ForeignKey(
        "Advert",
        on_delete=models.CASCADE,
        verbose_name="объявления",
        related_name="advert_contact",
    )
    phone_number = PhoneNumberField(verbose_name="номер телефона")

    class Meta:
        verbose_name = "номер для объявления"
        verbose_name_plural = "номера для объявлении"


class Promote(models.Model):
    class PromoteType(models.TextChoices):
        vip = "vip", "VIP"
        urgently = "urgently", "Срочно"
        highlighted = "highlighted", "выделенить"

    icon = models.ImageField(upload_to="promote/%Y/%m/%d", blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(verbose_name="описание")
    types = models.CharField(max_length=50, choices=PromoteType.choices)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Реклама"
        verbose_name_plural = "Рекламы"


class Advert(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="владелец"
    )
    name = models.CharField(max_length=150, verbose_name="название объявления")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="категория"
    )
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, verbose_name="подкатегория"
    )
    from_price = models.IntegerField(verbose_name="от цены")
    to_price = models.IntegerField(verbose_name="до цены")
    description = models.TextField(verbose_name="описание")
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="город")
    email = models.EmailField(verbose_name="E-mail")
    phone_number = PhoneNumberField(verbose_name="номер телефона")
    wa_number = PhoneNumberField(verbose_name="WhatsApp номер")
    promote = models.ForeignKey(
        Promote, on_delete=models.PROTECT, verbose_name="реклама", blank=True, null=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    image_count = models.IntegerField(verbose_name="количество изображений", default=0)
    view = models.IntegerField(verbose_name="просмотры", default=0)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and self.is_active and self.is_verified:
            client = connect(REDIS_HOST, REDIS_PORT)
            if not client.exists(self.category.name):
                client.set(self.category.name, 0)

            if not client.exists(self.sub_category.name):
                client.set(self.sub_category.name, 0)

            client.incr(self.category.name)
            client.incr(self.sub_category.name)
            self.category.set_advert_count(
                self.category, client.get(self.category.name)
            )
            self.sub_category.set_advert_count(
                self.category, client.get(self.sub_category.name)
            )

        super(Advert, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "объявление"
        verbose_name_plural = "объявлении"
