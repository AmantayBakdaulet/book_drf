from django_filters import rest_framework as filters
from .models import Book


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BookFilter(filters.FilterSet):
    genre = CharFilterInFilter(field_name='genre__name', lookup_expr='in')
    author = filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    publication_date__gte = filters.DateFilter(field_name='publication_date', lookup_expr='gte')
    publication_date__lte = filters.DateFilter(field_name='publication_date', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['genre', 'author', 'publication_date__gte', 'publication_date__lte']