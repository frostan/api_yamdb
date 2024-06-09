from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre


class GenreInline(admin.TabularInline):
    model = TitleGenre


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = (GenreInline,)
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category'
    )
    list_editable = ('category',)
    search_fields = ('year', 'name')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review',
        'text',
        'author',
        'pub_date'
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'score',
        'pub_date'
    )
