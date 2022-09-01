from django.db import models

from user.models import CustomUser
from advert.models import Advert


class Chat(models.Model):
    from_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="отправитель",
        related_name="from_user",
    )
    to_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="получатель",
        related_name="to_user",
    )
    message = models.TextField(verbose_name="сообщение")
    date = models.DateTimeField(auto_now=True, verbose_name="дата отправки")
    advert = models.ForeignKey(
        Advert, on_delete=models.CASCADE, verbose_name="объявление"
    )
    file = models.FileField(
        upload_to="chat/files/%Y/%m/%d/", blank=True, verbose_name="файл"
    )

    def __str__(self) -> str:
        return f"{self.from_user}"

    class Meta:
        verbose_name = "Сообщения"
        verbose_name_plural = "Сообщение"
