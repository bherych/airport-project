from django.db import models
from users.models import User
from flights.models import Flight

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

