from django.db import models
from countries.models import Country
from airlines.models import Airline

class Airport(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    airlines = models.ManyToManyField(Airline)
    

    def __str__(self):
        return f"{self.name} {self.country} ({self.code})"