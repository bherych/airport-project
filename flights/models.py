from django.db import models
from airplanes.models import Airplane
from airports.models import Airport

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
    # departure_time = models.DateTimeField()
    # arrival_time = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SCHEDULED)

    def __str__(self):
        return f"{self.flight_number} from {self.departure_airport} to {self.arrival_airport}, STATUS: {self.status}"