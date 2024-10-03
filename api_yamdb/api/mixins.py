from django.core.validators import RegexValidator
from rest_framework import serializers, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly


class UsernameFieldMixin(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')],
        required=True
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать это имя!')

        return value


class CategoryGenreMixin(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'delete')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
