from django.db import models

class Airline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    

    def __str__(self):
        return f"{self.name} ({self.code})"

class Airplane(models.Model):
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    capacity = models.IntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.manufacturer} {self.model} (Capacity: {self.capacity}) {self.airline}"

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Airport(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    airlines = models.ManyToManyField(Airline)
    

    def __str__(self):
        return f"{self.name} {self.country} ({self.code})"
    

