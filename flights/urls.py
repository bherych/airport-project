from rest_framework.routers import DefaultRouter
from .views import (
    FlightViewSet,
    TicketViewSet,
    SeatViewSet,
)

router = DefaultRouter()
router.register(r"flights", FlightViewSet, basename="flight")
router.register(r"tickets", TicketViewSet, basename="ticket")
router.register(r"seats", SeatViewSet, basename="seat")


urlpatterns = router.urls