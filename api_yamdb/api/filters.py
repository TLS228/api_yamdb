from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='exact')
    category = CharFilter(field_name='category__slug', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
