from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseCategoryGenreModel(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.name} - {self.slug}'


class Category(BaseCategoryGenreModel):
    pass


class Genre(BaseCategoryGenreModel):
    pass


class Title(models.Model):
    name = models.CharField(
        max_length=256,
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
        max_length=256,
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
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        """Строковое представление поля для админ-зоны."""
        return self.text


class Comment(models.Model):
    text = models.CharField(
        max_length=256,
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
