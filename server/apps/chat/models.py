from django.db import models

from user.models import CustomUser
from advert.models import Advert


class Room(models.Model):
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="получатель",
        related_name="room_owner_user",
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="отправитель",
        related_name="from_user_room",
    )
    advert = models.ForeignKey(
        Advert, on_delete=models.CASCADE, verbose_name="объявление"
    )

    def __str__(self) -> str:
        return f"{self.id}-{self.owner}-{self.user}"


class Chat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="канал")

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
    file = models.ImageField(
        upload_to="chat/files/%Y/%m/%d/", blank=True, verbose_name="файл"
    )

    def __str__(self) -> str:
        return f"{self.from_user}"

    class Meta:
        verbose_name = "Сообщения"
        verbose_name_plural = "Сообщение"
