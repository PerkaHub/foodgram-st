from django.db import models
from django.contrib.auth.models import AbstractUser

from foodgram.validators import AllowedCharactersUsernameValidator
from const.const import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_FIRST_LAST_NAME,
    MAX_LENGTH_USERNAME,
    AVATAR_UPLOAD_PATH,
)


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=MAX_LENGTH_FIRST_LAST_NAME
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=MAX_LENGTH_FIRST_LAST_NAME
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
    )
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        validators=[AllowedCharactersUsernameValidator()],
    )
    avatar = models.ImageField(
        verbose_name="Фото профиля",
        upload_to=AVATAR_UPLOAD_PATH
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
