from django.db import models
from airlines.models import Airplane, Airport
from users.models import User

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
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SCHEDULED)

    def __str__(self):
        return f"{self.flight_number} from {self.departure_airport} to {self.arrival_airport}, STATUS: {self.status}"
    


class Ticket(models.Model):
    class Status(models.TextChoices):
        BOOKED = 'booked', 'Booked'
        CANCELLED = 'cancelled', 'Cancelled'
        CHECKED_IN = 'used', 'Used'
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    # Should use PROTECT to avoid deleting flights with tickets but for testing purposese I leave it as CASCADE
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BOOKED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Ticket {self.id} - {self.user} - {self.flight} - {self.status}'

