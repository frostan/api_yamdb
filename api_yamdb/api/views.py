from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, status, permissions
from rest_framework.response import Response
from .permissions import AdminPermission, MyPermission
from api.serializers import (
    CategoriesSerializers,
    GenresSerializers,
    TitlesGetSerializers,
    TitlesPostSerializers,
    ReviewSerializers,
    CommentSerializers
)
from reviews.models import Categories, Genre, Title, Review, Comment
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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializers
        return TitlesPostSerializers


class CategorieViewSet(CreateDeleteListViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializers


class GenreViewSet(CreateDeleteListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс ViewSet модели Review."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    lookup_url_kwarg = 'review_id'
    permission_classes = (MyPermission, )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        """Переопределение метода create."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if serializer.is_valid():
            serializer.save(title=title, author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    """Класс ViewSet модели Comment."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    lookup_url_kwarg = 'comment_id'
    permission_classes = (MyPermission, )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        """Переопределение метода create."""
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
