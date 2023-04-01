from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet
from . import views

router = DefaultRouter()

router.register('categories', views.CategoriesViewSet,
                   basename='categories')
router.register('genres', views.GenresViewSet, basename='genres')
router.register('titles', views.TitlesViewSet, basename='titles')
router.register('users', UserViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
