from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from .filters import TitlesFilter

from api.permissions import (ReadOnly, IsAdmin, AccessOrReadOnly)


from .mixins import ListCreateDestroyViewSet

from users.models import User
from reviews.models import (Category, Genre, Title,
                            Review
                            )
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleCreateUpdateSerializer,
                          CommentSerializer, ReviewSerializer, UserSerializer
                          )

# from rest_framework.pagination import LimitOffsetPagination


HTTP_METHOD_NAMES = ('get', 'post', 'patch', 'delete')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    http_method_names = HTTP_METHOD_NAMES
    lookup_field = 'username'


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    # ordering_fields = ('id',)
    # ordering = ['id']

    # def get_queryset(self):
    #     return Category.objects.order_by('id')


class GenresViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    # ordering_fields = ('id',)

    # def get_queryset(self):
    #     return Genre.objects.order_by('id')


class TitlesViewSet(viewsets.ModelViewSet):
    # PUT - ?
    queryset = Title.objects.all().annotate(Avg("reviews__score"))
    serializer_class = TitleSerializer
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = (DjangoFilterBackend,)
    # фильтрует по имени и году?
    filterset_class = TitlesFilter
    # ordering_fields = ('id',)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleCreateUpdateSerializer
        return TitleSerializer

    # def get_queryset(self):
    #     return Title.objects.order_by('id')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          AccessOrReadOnly,)
    pagination_class = PageNumberPagination
    http_method_names = HTTP_METHOD_NAMES

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          AccessOrReadOnly,)
    pagination_class = PageNumberPagination
    http_method_names = HTTP_METHOD_NAMES

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        return review.comments.all()
