from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from user.models import CustomUser


class Category(models.Model):
    icon = models.ImageField(upload_to='category/icon/%Y/%m/%d', verbose_name='изображение категории')
    name = models.CharField(max_length=100, verbose_name='название категории')
    advert_count = models.IntegerField(verbose_name='количество объявлении')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=100, verbose_name='название подкатегори')
    advert_count = models.IntegerField(verbose_name='количество объявлении')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class AdvertImage(models.Model):
    image = models.ImageField(upload_to='advert/images/%Y/%m/%d')
    
    class Meta:
        verbose_name = 'изображение для объявлении'
        verbose_name_plural = 'изображении для объявлении'


class City(models.Model):
    name = models.CharField(max_length=150, verbose_name='название города')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class AdvertContact(models.Model):
    phone_number = PhoneNumberField(verbose_name='номер телефона')

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = 'номер для объявления'
        verbose_name_plural = 'номера для объявлении'


class Promote(models.Model):

    class PromoteType(models.TextChoices):
           vip = 'vip', 'VIP'
           urgently = 'urgently', 'Срочно'
           highlighted = 'highlighted', 'выделенить'

    icon = models.ImageField(upload_to='promote/%Y/%m/%d', blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(verbose_name='описание')
    
    types = models.CharField(max_length=50, choices=PromoteType.choices)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламы'



class Advert(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='владелец')
    name = models.CharField(max_length=150, verbose_name='название объявления')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name='подкатегория')
    from_price = models.IntegerField(verbose_name='от цены')
    to_price = models.IntegerField(verbose_name='до цены')
    description = models.TextField(verbose_name='описание')
    image = models.ForeignKey(AdvertImage, on_delete=models.CASCADE, verbose_name='изображение')
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='город')
    email = models.EmailField(verbose_name='E-mail')
    phone_number = PhoneNumberField(verbose_name='номер телефона')
    wa_number = PhoneNumberField(verbose_name='WhatsApp номер')
    contact = models.ForeignKey(AdvertContact, on_delete=models.PROTECT, verbose_name='доп номер телефона')
    promote = models.ForeignKey(Promote, on_delete=models.PROTECT, verbose_name='реклама', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    image_count = models.IntegerField(verbose_name='количество изображений')
    view = models.IntegerField(verbose_name='просмотры')
    is_active = models.BooleanField()
    is_verified = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявлении'



