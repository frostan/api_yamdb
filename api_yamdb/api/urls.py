from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from api.views import (
    CategorieViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
)

router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategorieViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='title_reviews',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='review_comments',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
]
