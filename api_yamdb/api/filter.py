from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title


class TitleFilters(FilterSet):
    """Кастомный фильтр для произведений."""

    name = CharFilter(field_name='name', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('year', 'genre', 'name', 'category')
