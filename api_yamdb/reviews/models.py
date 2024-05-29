from django.db import models
from django.contrib.auth import get_user_model

from api.const import (
    TEXT_MAX_LENGTH,
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH
)

User = get_user_model()


class BaseCategoryGenreModel(models.Model):
    """Базовая модель Категорий и Жанров."""

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.name} - {self.slug}'


class Category(BaseCategoryGenreModel):
    """Модель категории."""
    pass


class Genre(BaseCategoryGenreModel):
    """Модель жанров."""
    pass


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        default_related_name = 'titles'

    def __str__(self) -> str:
        return f'{self.category} - {self.genre} - {self.name} - {self.year}'


class TitleGenre(models.Model):
    """Модель жанров произведений."""

    title = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='genres',
        verbose_name='Жанр'
    )

    def str(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    """Модель Review."""

    text = models.CharField(
        max_length=TEXT_MAX_LENGTH,
        verbose_name='Текст'
    )
    score = models.IntegerField(default=1, verbose_name='Оценка')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='ID_произведения'
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор_отзыва'
    )

    class Meta:
        """Класс Мета."""

        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        """Строковое представление поля для админ-зоны."""
        return self.text


class Comment(models.Model):
    """Модель комментариев."""

    text = models.CharField(
        max_length=TEXT_MAX_LENGTH,
        verbose_name='Текст комментария'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Автор_комментария'
    )

    class Meta:
        """Класс Мета."""

        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Строковое представление поля для админ-зоны."""
        return self.text
