from .models import Flight, Ticket, Seat
from .serializers import FlightSerializer, TicketSerializer, SeatSerializer
from rest_framework import viewsets
import logging
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FlightFilter
from airport_project.permissions import ReadOnlyOrIsAdmin, IsOwnerOrAdmin
from rest_framework.exceptions import PermissionDenied


logger = logging.getLogger(__name__)

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().order_by('id')
    serializer_class = FlightSerializer
    permission_classes = [ReadOnlyOrIsAdmin]
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

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("You cannot create tickets manually.")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("You cannot update tickets.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("You cannot delete tickets.")
        return super().destroy(request, *args, **kwargs)

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [ReadOnlyOrIsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['flight', 'is_available']

    def list(self, request, *args, **kwargs):
        logger.info("Getting all seats request")
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving seats: {e}")
            raise

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving details of seat with id={kwargs.get('pk')}")
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving seat with id={kwargs.get('pk')}: {e}")
            raise

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating new seat: {request.data}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating seat: {e}")
            raise

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating seat with id={kwargs.get('pk')}: {request.data}")
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error updating seat with id={kwargs.get('pk')}: {e}")
            raise

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"Deleted seat with id={kwargs.get('pk')}")
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting seat with id={kwargs.get('pk')}: {e}")
            raise