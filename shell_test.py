import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airport_project.settings')
django.setup()

from airlines.models import Airline
from airplanes.models import Airplane
from airports.models import Airport
from countries.models import Country
from flights.models import Flight
from tickets.models import Ticket
from users.models import User
from airlines.serializers import AirlineSerializer
from airplanes.serializers import AirplaneSerializer
from airports.serializers import AirportSerializer
from countries.serializers import CountrySerializer
from flights.serializers import FlightSerializer
from tickets.serializers import TicketSerializer
from users.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io
from datetime import datetime

print("✅ Django shell environment initialized.")
print("📦 Imported: Airline, Airplane, Airport, Country, Flight, Ticket, User")
print("👉 You can now use them directly.")

import code
code.interact(local=locals())