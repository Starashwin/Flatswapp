import django_filters
from django import forms
from webapp_flatswapp.models import *
from django.db.models import Q

STATUS_ROOMS = (
(0, '0 bedroom'),
(1, '1 bedroom'),
(2, '2 bedrooms'),
(3, '3 bedrooms'),
(4, '4 bedrooms'),
(5, '5 bedrooms'),
(999, 'More than 5 bedrooms')
)

STATUS_FURNISHED = (
('Yes', 'Yes'),
('Partially', 'Partially'),
('No', 'No'),
)

class PropertyFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(field_name='name',lookup_expr='icontains' )
    address = django_filters.CharFilter(field_name='address',lookup_expr='icontains')
    n_bedrooms = django_filters.ChoiceFilter(field_name='n_bedrooms',choices=STATUS_ROOMS)
    furnished = django_filters.ChoiceFilter(field_name='furnished',choices=STATUS_FURNISHED)
    # beforedate = django_filters.DateFilter(field_name='outdata',lookup_expr='gt')
    # afterdate = django_filters.DateFilter(field_name='outdata',lookup_expr='lt')
    # greaterthanrent = django_filters.NumberFilter(field_name='rent',lookup_expr='gt')
    # lessthanrent = django_filters.NumberFilter(field_name='rent',lookup_expr='lt')
    price = django_filters.RangeFilter(field_name='rent')
    date = django_filters.DateFromToRangeFilter(field_name='outdata')
    multi_name_fields = django_filters.CharFilter(method='filter_by_all_name_fields')
    #year_joined__gt = django_filters.NumberFilter(name='date_joined', lookup_expr='outdata__gt')
    #year_joined__lt = django_filters.NumberFilter(name='date_joined', lookup_expr='outdata__lt')
    class Meta:
        model = Property
        fields = ['multi_name_fields','address','n_bedrooms','furnished','price','date']
         #groups = CombinedGroup(filters=['name', 'postcode'], combine=operator.or_)
    
    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(address__icontains=value) | Q(outward__icontains=value) | Q(description__icontains=value) | Q(nearest__icontains=value)| Q(neighbour__icontains=value))
