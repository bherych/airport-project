from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    TransactionViewSet,
    BuyTicketView,
    StrideWebhookView,
    payment_success,
    payment_cancel
    )
from django.urls import path, include

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"transactions", TransactionViewSet, basename="transaction")



urlpatterns = [
    path("buy-ticket/", BuyTicketView.as_view(), name="buy-ticket"),
    path("stripe/webhook/", StrideWebhookView.as_view(), name="stripe-webhook"),
    path("stripe/webhook/success/", payment_success, name="payment-success"),
    path("stripe/webhook/cancel/", payment_cancel, name="payment-cancel"),
    path("", include(router.urls)),
]