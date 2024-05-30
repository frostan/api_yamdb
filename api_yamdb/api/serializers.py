import datetime as dt

from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser
from api.const import (
    MAX_SCORE,
    MIN_SCORE,
    NAME_MAX_LENGTH,
    USERNAME_MAX_LEGTH
)


class CategorySerializers(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializers(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitlePostSerializers(serializers.ModelSerializer):
    """Cериализатор для POST запроса"""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = dt.date.today().year
        if not year >= value:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    def validate_name(self, value):
        if NAME_MAX_LENGTH < len(value):
            raise serializers.ValidationError(
                'Имя произведения большое 256 символов'
            )
        return value


class TitleGetSerializers(serializers.ModelSerializer):
    """Cериализатор для GET запроса"""

    category = CategorySerializers(read_only=True)
    genre = GenreSerializers(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class ReviewSerializers(serializers.ModelSerializer):
    """Cериализатор модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        """Класс Meta Cериализатора модели Review."""

        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date', 'title')
        read_only_fields = ('title', 'author')
        extra_kwargs = {'author': {'required': True}}

    def create(self, validated_data):
        """Переопределение метода Create."""
        title_id = self.context['view'].kwargs['title_id']
        author = validated_data.get('author')
        titles = list(
            Review.objects.values('title').filter(
                author=author))
        for title in titles:
            if title.get('title') == int(title_id):
                raise BadRequest('HTTP_400_BAD_REQUEST')
        review = Review.objects.create(**validated_data)
        return review

    def validate_score(self, value):
        """Проверка поля ."""
        if value not in range(MIN_SCORE, MAX_SCORE + 1):
            raise serializers.ValidationError(
                f'Оценка выходит за диапазон, {MIN_SCORE}..{MAX_SCORE}')
        return value


class CommentSerializers(serializers.ModelSerializer):
    """Cериализатор комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('title', 'author')

    def create(self, validated_data):
        """Переопределение метода Create."""
        title_id = self.context['view'].kwargs['title_id']
        review_id = self.context['view'].kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        if review.title_id != int(title_id):
            raise BadRequest('HTTP_400_BAD_REQUEST')
        comment = Comment.objects.create(**validated_data)
        return comment


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate_username(self, username):
        """Валидируем username."""
        if username == 'me':
            raise serializers.ValidationError(
                'me нельзя использовать в качестве username'
            )
        return username


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(max_length=USERNAME_MAX_LEGTH)
