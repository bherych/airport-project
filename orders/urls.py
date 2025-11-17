from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    TransactionViewSet,
    BuyTicketView,
    StrideWebhookView,
    )
from django.urls import path, include

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"transactions", TransactionViewSet, basename="transaction")



urlpatterns = [
    path("buy-ticket/", BuyTicketView.as_view(), name="buy-ticket"),
    path("webhook/stripe/", StrideWebhookView.as_view(), name="stripe-webhook"),
    path("", include(router.urls)),
]