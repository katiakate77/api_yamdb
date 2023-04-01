from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

# from .permissions import IsAdmin
from .serializers import UserSerializer
from users.models import User


HTTP_METHOD_NAMES = ['get', 'post', 'patch', 'delete']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = LimitOffsetPagination
    http_method_names = HTTP_METHOD_NAMES
    lookup_field = 'username'
