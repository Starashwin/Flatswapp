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
)

STATUS_FURNISHED = (
('Yes', 'Yes'),
('No', 'No'),
)

class PropertyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains' )
    postcode = django_filters.CharFilter(field_name='postcode',lookup_expr='icontains')
    n_bedrooms = django_filters.ChoiceFilter(field_name='n_bedrooms',choices=STATUS_ROOMS)
    furnished = django_filters.ChoiceFilter(field_name='furnished',choices=STATUS_FURNISHED)
    indate = django_filters.DateFilter(field_name='outdata',lookup_expr='gt')
    
    multi_name_fields = django_filters.CharFilter(method='filter_by_all_name_fields')
    #year_joined__gt = django_filters.NumberFilter(name='date_joined', lookup_expr='outdata__gt')
    #year_joined__lt = django_filters.NumberFilter(name='date_joined', lookup_expr='outdata__lt')
    class Meta:
        model = Property
        fields = ['name','postcode','indate','n_bedrooms','furnished','multi_name_fields',]
         #groups = CombinedGroup(filters=['name', 'postcode'], combine=operator.or_)
    
    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(postcode__icontains=value) | Q(description__icontains=value) | Q(nearest__icontains=value)| Q(neighbour__icontains=value))
