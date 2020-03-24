import django_filters
from django import forms
from webapp_flatswapp.models import *

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
    name = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')
    n_bedrooms = django_filters.ChoiceFilter(choices=STATUS_ROOMS)
    furnished = django_filters.ChoiceFilter(choices=STATUS_FURNISHED)
    #year_joined = django_filters.NumberFilter(name='date_joined', lookup_expr='year')
    #year_joined__gt = django_filters.NumberFilter(name='date_joined', lookup_expr='year__gt')
    #year_joined__lt = django_filters.NumberFilter(name='date_joined', lookup_expr='year__lt')
    class Meta:
        model = Property
        fields = ['name','address','n_bedrooms','furnished',]