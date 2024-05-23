import datetime as dt
from rest_framework import serializers

from reviews.models import Category, Genre, Title
#from users.models import CustomUser


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
    # rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            # 'rating',
            'description',
            'genre',
            'category'
        )
