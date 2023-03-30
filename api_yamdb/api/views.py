from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TitlesFilter
from .permissions import IsReadOnlyPermission, IsAdminPermission
from .mixins import ListCreateDestroyViewSet
from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleCreateUpdateSerializer)


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsReadOnlyPermission | IsAdminPermission]
    # permission_classes = [IsReadOnlyPermission | permissions.IsAdminUser]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = [IsReadOnlyPermission | IsAdminPermission]
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = [IsReadOnlyPermission | IsAdminPermission]
    filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('genre__slug',)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleCreateUpdateSerializer
        return TitleSerializer
