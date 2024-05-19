from django.urls import include, path
from rest_framework import routers

from api.views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
