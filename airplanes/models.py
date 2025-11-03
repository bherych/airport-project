from django.db import models
from airlines.models import Airline


class Airplane(models.Model):
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    capacity = models.IntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.manufacturer} {self.model} (Capacity: {self.capacity}) {self.airline}"