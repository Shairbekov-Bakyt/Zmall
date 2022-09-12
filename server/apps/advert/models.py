import os
import requests
from django.core.files.temp import NamedTemporaryFile

from django.db import models
from django.core.files import File

from phonenumber_field.modelfields import PhoneNumberField

from user.models import CustomUser


class Category(models.Model):
    icon = models.ImageField(
        upload_to="category/icon/%Y/%m/%d", verbose_name="иконка категории"
    )
    name = models.CharField(max_length=100, verbose_name="название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Под-категория",
        related_name="category_sub_category",
    )
    name = models.CharField(max_length=100, verbose_name="название подкатегори")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class AdvertImage(models.Model):
    advert = models.ForeignKey(
        "Advert",
        on_delete=models.CASCADE,
        verbose_name="объявления",
        related_name="advert_image",
    )
    image = models.ImageField()

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = "изображение для объявления"
        verbose_name_plural = "изображения для объявления"
    
    def get_remote_image(self, url):
        result = requests.get(url)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(result.content)
        img_temp.flush()

        self.image.save(os.path.basename(url), File(img_temp), save=True)

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
        verbose_name="объявление",
        related_name="advert_contact",
    )
    phone_number = PhoneNumberField(verbose_name="номер телефона")

    class Meta:
        verbose_name = "номер для объявления"
        verbose_name_plural = "номера для объявлении"


class AdvertView(models.Model):
    advert = models.OneToOneField(
        "Advert",
        on_delete=models.CASCADE,
        verbose_name="объявление",
        related_name="advert_view",
    )
    users = models.ManyToManyField(CustomUser)
    view = models.IntegerField(default=0)


class Promote(models.Model):
    class PromoteType(models.TextChoices):
        vip = "vip", "VIP"
        urgently = "urgently", "Срочно"
        highlighted = "highlighted", "Выделить"
    title = models.CharField(max_length=150)
    description = models.TextField(verbose_name="описание")
    price = models.IntegerField(verbose_name="цена")
    types = models.CharField(max_length=50, choices=PromoteType.choices)

    def __str__(self):
        return self.types

    class Meta:
        verbose_name = "Реклама"
        verbose_name_plural = "Рекламы"


class Advert(models.Model):
    class StatusChoice(models.TextChoices):
        active = "act", "Активный"
        inactive = "inact", "Неактивный"
        on_review = "on_r", "На проверке"

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="владелец",
        related_name="owner_advert",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="категория",
        related_name="category_advert",
    )
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        verbose_name="подкатегория",
        related_name="sub_category_product",
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        verbose_name="город",
        related_name="city_product",
    )
    promote = models.ManyToManyField(
        Promote,
        related_name="promote_advert",
        blank=True,
        verbose_name="реклама"
    )

    name = models.CharField(max_length=250, verbose_name="название объявления")
    description = models.TextField(verbose_name="описание")
    start_price = models.IntegerField(verbose_name="от цены")
    end_price = models.IntegerField(verbose_name="до цены")

    email = models.EmailField(verbose_name="E-mail")
    wa_number = PhoneNumberField(verbose_name="WhatsApp номер")

    created_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0, verbose_name='просмотры')
    status = models.CharField(
        max_length=10,
        verbose_name="статус",
        choices=StatusChoice.choices,
        default=StatusChoice.on_review,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "объявление"
        verbose_name_plural = "объявления"


class FavoriteAdvert(models.Model):
    adverts = models.ManyToManyField(Advert, related_name='favorite_adverts', verbose_name='объявление')
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='favorite_user', verbose_name='клиент')
    
    def __str__(self):
        return f"id : {self.id}"

    class Meta:
        verbose_name = 'Избранный продукт'
        verbose_name_plural = 'Избранные продукты'


class Comment(models.Model):
    advert = models.ForeignKey(
        Advert,
        on_delete=models.CASCADE,
        related_name="advert_comment",
        verbose_name="объявление"
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_comment",
        verbose_name="пользователь"

    )
    parent = models.ForeignKey(
        'self',
        verbose_name="Комментарий-родитель ",
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="children"
    )
    text = models.TextField(
        verbose_name="текст комментария",
        max_length=5000
    )

    def __str__(self):
        return f"{self.advert} - comment"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя')
    email = models.EmailField(max_length=100, verbose_name='E-mail')
    feedback_title = models.CharField(max_length=150, verbose_name='тема сообщение')
    message = models.TextField(verbose_name='сообщение')

    def __str__(self):
        return self.name


class HelpCategory(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Help(models.Model):
    help_category = models.ForeignKey(HelpCategory, on_delete=models.CASCADE)
    question = models.CharField(max_length=150, verbose_name='вопрос')
    answer = models.TextField(verbose_name='ответ')
    view = models.IntegerField(default=0)

    def __str__(self):
        return self.question


class FooterLink(models.Model):
    class SocialNetworkChoice(models.TextChoices):
        instagram = "instagram", "instagram"
        facebook = "facebook", "facebook"
        ok = "ok", "ok"
        google_play = 'google_play', 'google_play'

    link = models.URLField(verbose_name='cсылка')
    status = models.CharField(
        max_length=100,
        verbose_name="статус",
        choices=SocialNetworkChoice.choices,
    )

    def __str__(self):
        return self.link
