from django.contrib import admin
from .models import Flight, Ticket, Seat

admin.site.register(Flight)
admin.site.register(Ticket)
admin.site.register(Seat)