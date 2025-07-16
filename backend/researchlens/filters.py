"""This module contains filters for the ResearchLens application, allowing for filtering of research papers based on various criteria."""

from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFilter, CharFilter
from .models import Paper

class PaperFilter(FilterSet):
    start_date = DateFilter(field_name='published_date', lookup_expr='gte')
    end_date = DateFilter(field_name='published_date', lookup_expr='lte')
    categories = CharFilter(field_name='categories', lookup_expr='in', method='filter_categories')

    def filter_categories(self, queryset, name, value):
        category_list = value.split(',')
        return queryset.filter(categories__in=category_list)

    class Meta:
        model = Paper
        fields = ['start_date', 'end_date', 'categories']
