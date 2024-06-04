from django.db import models
from django.contrib.auth.models import AbstractUser

from api.const import (
    ROLE_MAX_LEGTH,
    CODE_MAX_LEGTH,
    EMAIL_MAX_LEGTH
)


class CustomUser(AbstractUser):
    """Кастомная модель юзера."""
    USER_ROLES = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ')
    ]
    bio = models.TextField('Биография', blank=True)
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=EMAIL_MAX_LEGTH
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        null=True,
        blank=True,
        max_length=CODE_MAX_LEGTH
    )
    role = models.CharField(
        'Вид пользователя',
        default='user',
        choices=USER_ROLES,
        max_length=ROLE_MAX_LEGTH
    )

    @property
    def is_admin(self):
        """Атрибут класса."""
        return self.role == 'admin' or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
