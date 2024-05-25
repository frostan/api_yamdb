import datetime as dt
from django.core.exceptions import BadRequest
from rest_framework import serializers
from reviews.models import Categories, Genre, Title, Review, Comment
from users.models import CustomUser

# Максимальная оценка.
MAX_SCORE = 10
# Минимальная оценка.
MIN_SCORE = 1

class CategoriesSerializers(serializers.ModelSerializer):

    class Meta:
        model = Categories
        exclude = ('id',)


class GenresSerializers(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitlesPostSerializers(serializers.ModelSerializer):
    """Cериализатор для POST запроса"""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )
        
    def get_rating(self, obj):
        """Функция для расчета поля rating."""
        scores = list(Review.objects.values('score').filter(
                title__id=obj.id))
        ratings = 0
        for score in scores:
            ratings += score.get('score')
        rating = ratings / len(scores)
        return rating


class ReviewSerializers(serializers.ModelSerializer):
    """Cериализатор ."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )


    class Meta:
        model = Review
#        fields = ('id', 'text', 'score', 'author', 'pub_date', 'title')
        fields = ('id', 'text', 'score', 'author', 'pub_date', 'title')
        read_only_fields = ('title',)

    def create(self, validated_data):
        """Переопределение метода Create."""
        title_id = self.context['view'].kwargs['title_id']
        author = validated_data.get('author')
        titles = list(
            Review.objects.values('title').filter(
                author=author))
        for title in titles:
            print('title==============', title.get('title'), type(title.get('title')))
            if title.get('title') == int(title_id):
                print('BadRequest==============')
                raise BadRequest("HTTP_400_BAD_REQUEST")
        review = Review.objects.create(**validated_data)
        return review

    def validate_score(self, value):
        if value not in range(MIN_SCORE, MAX_SCORE + 1):
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
