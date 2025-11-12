import django_filters
from .models import Airplane

class AirplaneFilter(django_filters.FilterSet):
    model = django_filters.CharFilter(field_name='model', lookup_expr='icontains')
    manufacturer = django_filters.CharFilter(field_name='manufacturer', lookup_expr='icontains')
    capacity_min = django_filters.NumberFilter(field_name='capacity', lookup_expr='gte')
    capacity_max = django_filters.NumberFilter(field_name='capacity', lookup_expr='lte')
    airline = django_filters.CharFilter(field_name='airline__name', lookup_expr='icontains')

    class Meta:
        model = Airplane
        fields = ['model', 'manufacturer', 'capacity_min', 'capacity_max', 'airline']