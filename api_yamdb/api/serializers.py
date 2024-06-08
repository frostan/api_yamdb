from rest_framework import serializers
from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api_yamdb.settings import EMAIL
from api.const import (
    MAX_SCORE,
    MIN_SCORE,
    USERNAME_MAX_LENGTH,
    CODE_MAX_LENGTH,
)
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

    class Meta:
        """Класс Meta Cериализатора модели Review."""

        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        extra_kwargs = {'author': {'required': True}}

    def validate(self, data):
        """Проверка существования записи с title_id и author."""
        if self.partial:
            return data
        title_id = int(self.context['view'].kwargs['title_id'])
        author = self.context['request'].user
        titles = Review.objects.values('title').filter(
            title=title_id, author=author).exists()
        if titles:
            raise BadRequest('HTTP_400_BAD_REQUEST')
        return data

    def validate_score(self, value):
        """Проверка поля score."""
        if value < MIN_SCORE or value > MAX_SCORE:
            raise serializers.ValidationError(
                f'Оценка выходит за диапазон, {MIN_SCORE}..{MAX_SCORE}')
        return value


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
        title_id = self.context['view'].kwargs['title_id']
        review_id = self.context['view'].kwargs['review_id']
        get_object_or_404(Review, id=review_id)
        reviews = Review.objects.filter(
            id=review_id, title=title_id).exists()
        if not reviews:
            raise BadRequest('HTTP_400_BAD_REQUEST')
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


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=USERNAME_MAX_LENGTH
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, username):
        """Валидируем username."""
        if username == 'me':
            raise serializers.ValidationError(
                'me нельзя использовать в качестве username'
            )
        return username

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        try:
            user = User.objects.get(username=username, email=email)
        except ObjectDoesNotExist:
            user = User.objects.create(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Ваш код: {confirmation_code}',
            EMAIL,
            [email],
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
