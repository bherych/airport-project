from rest_framework import serializers
from .models import Flight, Ticket, Seat

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            'id',
            'flight_number',
            'departure_airport',
            'arrival_airport',
            'departure_time',
            'arrival_time',
            'airplane',
            'status',
        ]



class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'id',
            'user',
            'flight',
            'status',
            'seat_number',
            'price',
            'order',
            'created_at',
            'updated_at',
        ]

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = [
            'id',
            'flight',
            'seat_number',
            'is_available',
        ]