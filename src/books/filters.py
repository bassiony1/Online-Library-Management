import django_filters
from .models import book


class BookFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr= 'icontains')
    class Meta:
        model = book
        fields = [ 'name' , 'category' ]
