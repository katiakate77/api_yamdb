from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Использовать "me" в качестве username запрещено'
        )
    return value


def modify_fields(**kwargs):
    def wrap(cls):
        for field, properties_dict in kwargs.items():
            for prop, val in properties_dict.items():
                setattr(cls._meta.get_field(field), prop, val)
        return cls
    return wrap


@modify_fields(username={
    'validators': [UnicodeUsernameValidator(), validate_username]})
class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    role = models.CharField(
        max_length=30,
        choices=USER_ROLES,
        default=USER,
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=36,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
