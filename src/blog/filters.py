import django_filters
from .models import post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr= 'icontains')
    class Meta:
        model = post
        fields = [ 'title' ]
