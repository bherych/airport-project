from django.db import models
from django.contrib.auth.models import User

class User(User):
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username

