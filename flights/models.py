from django.db import models
from airlines.models import Airplane, Airport
from django.conf import settings
from orders.models import Order

class Flight(models.Model):

    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        DEPARTED = 'departed', 'Departed'
        ARRIVED = 'arrived', 'Arrived'
        CANCELLED = 'cancelled', 'Cancelled'
        DELAYED = 'delayed', 'Delayed'

    flight_number = models.CharField(max_length=10)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    departure_time = models.DateTimeField(blank=True, null=True)
    arrival_time = models.DateTimeField(blank=True, null=True)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SCHEDULED)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number} from {self.departure_airport} to {self.arrival_airport}, STATUS: {self.status}"
    
class Seat(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'Seat {self.seat_number} on {self.flight.airplane}'

class Ticket(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        BOOKED = 'booked', 'Booked'
        CANCELLED = 'cancelled', 'Cancelled'
        CHECKED_IN = 'used', 'Used'
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name='tickets')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    seat_number = models.CharField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Ticket {self.id} - {self.user} - {self.flight} - {self.status}'