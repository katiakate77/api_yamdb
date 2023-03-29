from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Email'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия пользователя'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.TextField(
        max_length=30,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
