from rest_framework import mixins, serializers, viewsets
from rest_framework.filters import SearchFilter

from reviews.constants import MAX_USERNAME_LENGTH
from .permissions import IsAdminOrReadOnly
from .validators import username_validator


class UsernameValidatorMixin:

    def validate_username(self, value):
        return username_validator(value)


class UsernameFieldMixin(UsernameValidatorMixin, serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        required=True
    )


class CategoryGenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
