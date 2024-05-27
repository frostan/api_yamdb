from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import filters, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .permissions import AdminPermission
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
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
from reviews.models import Category, Genre, Title, Review, Comment


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
        title = Title.objects.get(id=title_id)
        if serializer.is_valid():
            serializer.save(title=title, author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователя."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AdminPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if serializer.validated_data.get('role'):
                if request.user.role != 'admin' or (
                    request.user.is_authenticated
                ):
                    serializer.validated_data['role'] = request.user.role
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """Вью токена."""

    def post(self, request):
        """POST-запрос на получение токена."""
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(CustomUser, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response({'token': token}, status=status.HTTP_200_OK)


class SignUpView(APIView):
    """Вью регистрации."""

    def post(self, request):
        """POST-запрос на получения email с кодом подтверждения."""
        serializer = SignUpSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        if not serializer.is_valid():
            try:
                CustomUser.objects.get(username=username, email=email)
            except ObjectDoesNotExist:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        user, created = CustomUser.objects.get_or_create(
            username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Ваш код : {confirmation_code}',
            'uu@yamnd.com',
            [email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
