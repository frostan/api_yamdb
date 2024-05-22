from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import filters, mixins, viewsets, status
from rest_framework.response import Response

from .permissions import AdminPermission

from api.serializers import (
    CategoriesSerializers,
    GenresSerializers,
    TitlesGetSerializers,
    TitlesPostSerializers,
    CustomUserSerializer,
    SignUpSerializer,
    ReviewSerializers,
    CommentSerializers
)
from users.models import CustomUser
from reviews.models import Categories, Genres, Titles, Review, Comment


class CreateDeleteListViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
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
    queryset = Genres.objects.all()
    serializer_class = GenresSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = (AdminPermission,)

    def get_queryset(self):
        """Переопределение queryset."""
        title_id = self.kwargs.get('title_id')
        print("@@@@@@@@@@@@@@@@@@@", Review.objects.filter(title=title_id))
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer):
        """Переопределение метода create."""
        title_id = self.kwargs.get('title_id')
        title = Titles.objects.get(id=title_id)
        if serializer.is_valid():
            serializer.save(title=title, author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('username',)


class SignUpViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer


class TokenViewSet(TokenViewBase):
    pass
