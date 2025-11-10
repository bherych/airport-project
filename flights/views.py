from .models import Flight, Ticket
from .serializers import FlightSerializer, TicketSerializer
from rest_framework import viewsets

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer