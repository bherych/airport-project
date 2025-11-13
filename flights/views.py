from .models import Flight, Ticket
from .serializers import FlightSerializer, TicketSerializer
from rest_framework import viewsets
import logging
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FlightFilter


logger = logging.getLogger(__name__)

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().order_by('id')
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightFilter

    def list(self, request, *args, **kwargs):
        logger.info("Getting all flight request")
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving flights: {e}")
            raise

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving details of flight with id={kwargs.get('pk')}")
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving flight with id={kwargs.get('pk')}: {e}")
            raise

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating new flight: {request.data}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating flight: {e}")
            raise

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating flight with id={kwargs.get('pk')}: {request.data}")
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error updating flight with id={kwargs.get('pk')}: {e}")
            raise

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"Deleting flight with id={kwargs.get('pk')}")
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting flight with id={kwargs.get('pk')}: {e}")
            raise

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'user', 'flight']


    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(passenger=user)
        

    def list(self, request, *args, **kwargs):
        logger.info("Getting all tickets request")
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving tickets: {e}")
            raise

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving details of ticket with id={kwargs.get('pk')}")
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving ticket with id={kwargs.get('pk')}: {e}")
            raise

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating new ticket: {request.data}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating ticket: {e}")
            raise

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating ticket with id={kwargs.get('pk')}: {request.data}")
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error updating ticket with id={kwargs.get('pk')}: {e}")
            raise

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"Deleted ticket with id={kwargs.get('pk')}")
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting ticket with id={kwargs.get('pk')}: {e}")
            raise