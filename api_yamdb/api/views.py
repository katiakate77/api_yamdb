from rest_framework import filters, permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from rest_framework.decorators import action
from rest_framework.response import Response


from .filters import TitlesFilter

from api.permissions import (ReadOnly, IsAdmin, AccessOrReadOnly)


from .mixins import ListCreateDestroyViewSet

from users.models import User
from reviews.models import (Category, Genre,
                            Review, Title,
                            )
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ProfileSerializer, ReviewSerializer,
                          TitleSerializer, TitleCreateUpdateSerializer,
                          UserSerializer, ProfileSerializer
                          )


HTTP_METHOD_NAMES = ('get', 'post', 'patch', 'delete')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter
                       )
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    http_method_names = HTTP_METHOD_NAMES
    lookup_field = 'username'
    ordering = ('id',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        serializer_class=ProfileSerializer,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter
                       )
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('id',)


class GenresViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ReadOnly | IsAdmin]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,
                       filters.OrderingFilter
                       )
    search_fields = ('name',)
    ordering = ('id',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg("reviews__score"))
    serializer_class = TitleSerializer
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter
                       )
    http_method_names = HTTP_METHOD_NAMES
    filterset_class = TitlesFilter
    ordering = ('id',)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleCreateUpdateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          AccessOrReadOnly,)
    pagination_class = PageNumberPagination
    http_method_names = HTTP_METHOD_NAMES
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id',)

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
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id',)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        return review.comments.all()
