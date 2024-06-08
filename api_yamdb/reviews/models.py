from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from api.const import (
    TEXT_MAX_LENGTH,
    NAME_MAX_LENGTH,
    MIN_SCORE,
    MAX_SCORE,
    TEXT_ADMIN_ZONE_MAX_LENGTH
)
from reviews.validators import validate_year

User = get_user_model()


class BaseCategoryGenreModel(models.Model):
    """Базовая модель Категорий и Жанров."""

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name} - {self.slug}'


class BaseCommentReviewModel(models.Model):
    """Базовая модель Комментарий и Оценки."""

    text = models.CharField(
        max_length=TEXT_MAX_LENGTH,
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор_'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        """Строковое представление поля для админ-зоны."""
        return self.text[:TEXT_ADMIN_ZONE_MAX_LENGTH]


class Category(BaseCategoryGenreModel):
    """Модель категории."""

    class Meta(BaseCategoryGenreModel.Meta):
        verbose_name = 'Категории'


class Genre(BaseCategoryGenreModel):
    """Модель жанров."""

    class Meta(BaseCategoryGenreModel.Meta):
        verbose_name = 'Жанры'


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название'
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year]
    )
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
        related_name='titles_genres',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles_genres',
        verbose_name='Жанр'
    )

    def str(self):
        return f'{self.title} - {self.genre}'


class Review(BaseCommentReviewModel):
    """Модель Review."""

    score = models.PositiveSmallIntegerField(
        default=MIN_SCORE,
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE)
        ],
        verbose_name='Оценка'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='ID_произведения'
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
        default_related_name = 'reviews'


class Comment(BaseCommentReviewModel):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Отзыв'
    )

    class Meta:
        """Класс Мета."""

        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
