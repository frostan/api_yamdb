from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from api.serializers import (
    CategoriesSerializers,
    GenresSerializers,
    TitlesGetSerializers,
    TitlesPostSerializers,
)
from reviews.models import Category, Genre, Title
# from users.models import CustomUser


class CreateDeleteListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializers
        return TitlesPostSerializers


class CategoriesViewSet(CreateDeleteListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializers


class GenresViewSet(CreateDeleteListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializers
