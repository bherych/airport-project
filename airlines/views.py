from rest_framework import generics
from .models import Airline, Airplane, Airport, Country
from .serializers import AirlineSerializer, AirplaneSerializer, AirportSerializer, CountrySerializer

class AirlineListCreateView(generics.ListCreateAPIView):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer

class AirplaneListCreateView(generics.ListCreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

class AirportListCreateView(generics.ListCreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class CountryListCreateView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class AirlineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer

class AirplaneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

class AirportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
