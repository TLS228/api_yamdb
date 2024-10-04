from django.core.validators import RegexValidator
from rest_framework import serializers, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly


USERNAME_MAX_LENGTH = 150
USERNAME_REGEX = r'^[\w.@+-]+\Z'
USERNAME_ME_ERROR_MESSAGE = 'Запрещено использовать это имя!'


class UsernameFieldMixin(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[RegexValidator(regex=USERNAME_REGEX)],
        required=True
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(USERNAME_ME_ERROR_MESSAGE)

        return value


class CategoryGenreMixin(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'delete')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
