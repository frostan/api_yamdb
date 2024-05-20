from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Кастомная модель юзера."""
    USER_ROLES = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ')
    ]
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=256
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        null=True,
        blank=True,
        max_length=256
    )
    user_role = models.CharField(
        'Вид пользователя',
        default='user',
        choices=USER_ROLES,
        max_length=20
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
