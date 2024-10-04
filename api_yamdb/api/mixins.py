import re

from django.core.validators import RegexValidator
from rest_framework import serializers, status, viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly
from reviews.constants import MAX_USERNAME_LENGTH, USERNAME_REGEX


class UsernameFieldMixin(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        required=True
    )

    def validate_username(self, value):
        if value == 'me' or not re.match(USERNAME_REGEX, value):
            raise serializers.ValidationError('Запрещено использовать это имя!')
        return value


class CategoryGenreViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
