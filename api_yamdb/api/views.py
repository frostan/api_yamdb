from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, status, permissions
from rest_framework.response import Response
from .permissions import AdminPermission, MyPermission
from django.shortcuts import get_object_or_404

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


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializers
        return TitlesPostSerializers


class CategoriesViewSet(CreateDeleteListViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializers


class GenresViewSet(CreateDeleteListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = (MyPermission, )
    http_method_names = ['get', 'post', 'patch', 'delete'] 

    def get_queryset(self):
        """Переопределение queryset."""
        title_id = self.kwargs.get("title_id")
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset
    
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)     

    def perform_create(self, serializer):
        """Переопределение метода create."""
        title_id = self.kwargs.get('title_id')
#        title = Title.objects.get(id=title_id)
        title = get_object_or_404(Title, id=title_id)
        if serializer.is_valid():
            serializer.save(title=title, author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def perform_update(self, serializer):
    #     """Переопределение метода update."""
    #     title_id
    #     title_id = self.kwargs.get('title_id')
    #     title = Titles.objects.get(id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
