from django.db import models

#from users.models import CustomUser


class BaseCategoriesGenresModel(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.name} - {self.slug}'


class Categories(BaseCategoriesGenresModel):
    pass


class Genres(BaseCategoriesGenresModel):
    pass


class Titles(models.Model):
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
        Genres,
        verbose_name='Slug жанра'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Slug категории'
    )

    class Meta:
        default_related_name = 'titles'

    def __str__(self) -> str:
        return f'{self.category} - {self.genre} - {self.name} - {self.year}'
