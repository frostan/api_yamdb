from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.const import (
    CODE_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
    MAX_SCORE,
    MIN_SCORE,
    USERNAME_MAX_LENGTH,
    CODE_MAX_LENGTH
)
from api_yamdb.settings import EMAIL
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """Cериализатор для произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True,
        allow_empty=False
    )
    rating = serializers.IntegerField(default=0, read_only=True)

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

    def to_representation(self, value):
        serializer = super().to_representation(value)
        serializer['genre'] = GenreSerializer(
            value.genre.all(), many=True
        ).data
        serializer['category'] = CategorySerializer(
            value.category
        ).data
        return serializer


class ReviewSerializer(serializers.ModelSerializer):
    """Cериализатор модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.IntegerField()

    class Meta:
        """Класс Meta Cериализатора модели Review."""

        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """Проверка существования Отзыва c title_id и author."""
        if self.partial:
            return data
        title_id = int(self.context['view'].kwargs['title_id'])
        author = self.context['request'].user
        titles = Review.objects.values('title').filter(
            title=title_id, author=author).exists()
        if titles:
            raise serializers.ValidationError(
                'Нельзя делать повторный Отзыв одного и того же произведения'
            )
        return data

    def validate_score(self, value):
        """Проверка поля score."""
        if MIN_SCORE <= value <= MAX_SCORE:
            return value
        raise serializers.ValidationError(
            f'Оценка выходит за диапазон, {MIN_SCORE}..{MAX_SCORE}')


class CommentSerializer(serializers.ModelSerializer):
    """Cериализатор комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

    def validate(self, data):
        """Проверка существования записи с title_id и review_id."""
        if self.partial:
            return data
        review_id = self.context['view'].kwargs['review_id']
        get_object_or_404(Review, id=review_id)
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class SignUpSerializer(serializers.Serializer):
    """Сериализатор регистрации."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=USERNAME_MAX_LENGTH,
        required=True
    )
    email = serializers.EmailField(required=True, max_length=EMAIL_MAX_LENGTH)

    def validate_username(self, username):
        """Валидируем username."""
        if username == 'me':
            raise serializers.ValidationError(
                'me нельзя использовать в качестве username'
            )
        return username

    def validate(self, data):
        try:
            User.objects.get_or_create(
                username=data.get('username'),
                email=data.get('email')
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Такой username или email уже существует'
            )
        return data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Ваш код: {confirmation_code}',
            EMAIL,
            [validated_data.get('email')],
        )
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH
    )
    confirmation_code = serializers.CharField(
        required=True, max_length=CODE_MAX_LENGTH
    )
