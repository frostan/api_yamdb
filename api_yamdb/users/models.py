from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from api.const import EMAIL_MAX_LENGTH, ROLE_MAX_LENGTH


class User(AbstractUser):
    """Кастомная модель юзера."""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    USER_ROLES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ')
    ]

    bio = models.TextField('Биография', blank=True)
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=EMAIL_MAX_LENGTH
    )

    role = models.CharField(
        'Вид пользователя',
        default=USER,
        choices=USER_ROLES,
        max_length=ROLE_MAX_LENGTH
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def clean(self):
        if self.username == 'me':
            raise ValidationError(
                {'username': 'me нельзя использовать в качестве username'}
            )

    @property
    def is_admin(self):
        """Атрибут класса."""
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
