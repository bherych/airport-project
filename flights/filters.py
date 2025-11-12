import django_filters
from .models import Flight

class FlightFilter(django_filters.FilterSet):
    departure_after = django_filters.DateTimeFilter(field_name='departure_time', lookup_expr='gte')
    departure_before = django_filters.DateTimeFilter(field_name='departure_time', lookup_expr='lte')
    arrival_after = django_filters.DateTimeFilter(field_name='arrival_time', lookup_expr='gte')
    arrival_before = django_filters.DateTimeFilter(field_name='arrival_time', lookup_expr='lte')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = Flight
        fields = ['departure_airport', 'arrival_airport', 'status']