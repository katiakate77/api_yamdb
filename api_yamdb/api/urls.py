from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet


router = DefaultRouter()

router.register('users', UserViewSet)

app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
