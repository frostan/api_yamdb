import datetime as dt
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import CustomUser

# Максимальная оценка.
MAX_SCORE = 10
# Минимальная оценка.
MIN_SCORE = 1


class CategoriesSerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class GenresSerializers(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitlesPostSerializers(serializers.ModelSerializer):
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


class TitlesGetSerializers(serializers.ModelSerializer):
    """Cериализатор для GET запроса"""
    category = CategoriesSerializers(read_only=True)
    genre = GenresSerializers(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'reviews',
            'description',
            'genre',
            'category'
        )


class ReviewSerializers(serializers.ModelSerializer):
    """Cериализатор ."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'title', 'author', 'pub_date')

    def validate_score(self, value):
        if value in range(MIN_SCORE, MAX_SCORE + 1):
            raise serializers.ValidationError(
                f'Оценка выходит за диапазон, {MIN_SCORE}..{MAX_SCORE}')
        return value


class CommentSerializers(serializers.ModelSerializer):
    """Cериализатор ."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'pub_date')


class CustomUserSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                ' me нельзя использовать в качестве username'
            )
        return username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=250)
