import django_filters
from django.contrib.auth.models import User
from .models import Profile

class ProfilesFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr= 'icontains')
    last_name = django_filters.CharFilter(lookup_expr= 'icontains')
    username = django_filters.CharFilter(lookup_expr= 'icontains')
    class Meta:
        model = User
        fields = [ 'username' , 'first_name' , 'last_name']
