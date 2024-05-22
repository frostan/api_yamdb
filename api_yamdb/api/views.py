from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import filters, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .permissions import AdminPermission

from api.serializers import (
    CategoriesSerializers,
    GenresSerializers,
    TitlesGetSerializers,
    TitlesPostSerializers,
    CustomUserSerializer,
    ReviewSerializers,
    CommentSerializers,
    TokenSerializer,
    SignUpSerializer,
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

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True)
            if not (serializer.is_valid()):
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if serializer.validated_data.get('role'):
                if request.user.role != 'admin' or not (
                    request.user.is_authenticated
                ):
                    serializer.validated_data['role'] = request.user.role
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_view(request):
    serializer = TokenSerializer(data=request.data)
    if not (serializer.is_valid()):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_cade')
    user = get_object_or_404(CustomUser, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response(data={'token': token}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = SignUpSerializer(data=request.data)
    username = request.data.get('username')
    email = request.data.get('email')
    if not (serializer.is_valid()):
        CustomUser.objects.all(username=username, email=email)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user, created = CustomUser.objects.get_or_create(
        username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код для регистрации',
        f'Ваш код {confirmation_code}',
        'uu@yamd.com',
        [email],
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
