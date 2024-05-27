from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title


class TitleFilters(FilterSet):
    name = CharFilter(field_name='name')
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('year',)
