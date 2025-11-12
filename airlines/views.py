from .models import Airline, Airplane, Airport, Country
from .serializers import AirlineSerializer, AirplaneSerializer, AirportSerializer, CountrySerializer
from rest_framework import viewsets
import logging
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AirplaneFilter

logger = logging.getLogger(__name__)

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'country']
    

    def list(self, request, *args, **kwargs):
        logger.info("Got all airlines request")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieved details of airline with id={kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Created new airline: {request.data}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating airline with id={kwargs.get('pk')}: {request.data}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"Deleted airline with id={kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = AirplaneFilter

    def list(self, request, *args, **kwargs):
        logger.info("Got all airplane request")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieved details of airplane with id={kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Created new airplane: {request.data}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating airplane with id={kwargs.get('pk')}: {request.data}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"Deleted airplane with id={kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'city', 'country']

    def list(self, request, *args, **kwargs):
        logger.info("Got all airport request")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieved details of airport with id={kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Created new airport: {request.data}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating airport with id={kwargs.get('pk')}: {request.data}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"Deleted airport with id={kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'code']

    def list(self, request, *args, **kwargs):
        logger.info("Got all countries request")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieved details of country with id={kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Created new country: {request.data}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating country with id={kwargs.get('pk')}: {request.data}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"Deleted country with id={kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)