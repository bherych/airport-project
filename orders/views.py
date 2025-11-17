from .models import Order, Transaction
from .serializers import OrderSerializer, TransactionSerializer
import logging
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
import stripe
from airport_project.permissions import IsOwnerOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Response
from rest_framework import viewsets
from flights.models import Flight, Seat, Ticket
import os
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


logger = logging.getLogger(__name__)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'user']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        logger.info("Getting all order request")
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving orders: {e}")
            raise

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"User {request.user.id} retrieving order id={kwargs.get('pk')}")
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving order {kwargs.get('pk')} for user {request.user.id}: {e}")
            raise

    def create(self, request, *args, **kwargs):
        logger.info(f"User {request.user.id} creating new order: {request.data}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating order for user {request.user.id}: {e}")
            raise

    def update(self, request, *args, **kwargs):
        logger.info(f"User {request.user.id} updating order {kwargs.get('pk')}: {request.data}")
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error updating order {kwargs.get('pk')} for user {request.user.id}: {e}")
            raise

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"User {request.user.id} deleting order id={kwargs.get('pk')}")
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting order {kwargs.get('pk')} for user {request.user.id}: {e}")
            raise

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'user', 'order']

    def list(self, request, *args, **kwargs):
        logger.info("Getting all transaction request")
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving transactions: {e}")
            raise

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving details of transaction with id={kwargs.get('pk')}")
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving transaction with id={kwargs.get('pk')}: {e}")
            raise

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating new transaction: {request.data}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            raise

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating transaction with id={kwargs.get('pk')}: {request.data}")
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error updating transaction with id={kwargs.get('pk')}: {e}")
            raise

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"Deleting transaction with id={kwargs.get('pk')}")
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting transaction with id={kwargs.get('pk')}: {e}")
            raise

class BuyTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        flight_id = request.data.get("flight")
        seat_numbers = request.data.get("seats", [])

        if not isinstance(seat_numbers, list):
            seat_numbers = [seat_numbers]

        flight = Flight.objects.get(id=flight_id)

        seats = Seat.objects.filter(
            flight=flight,
            seat_number__in=seat_numbers,
            is_available=True
        )

        if seats.count() != len(seat_numbers):
            return Response(
                {"error": "One or more seats are not available"},
                status=400
            )

        total_price = flight.price * len(seat_numbers)

        order = Order.objects.create(
            user=user,
            status="pending",
            total_price=total_price
        )

        tickets = []
        for seat in seats:
            ticket = Ticket.objects.create(
                user=user,
                flight=flight,
                seat_number=seat.seat_number,
                price=flight.price,
                order=order
            )
            tickets.append(ticket)
            seat.is_available = False
            seat.save()

        DOMAIN = os.getenv("DOMAIN", "http://localhost:8000")

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": f"Flight {flight.id}"},
                        "unit_amount": int(flight.price * 100),
                    },
                    "quantity": len(seats),
                }
            ],
            mode="payment",
            success_url=DOMAIN + "/success?order_id=" + str(order.id),
            cancel_url=DOMAIN + "/cancel?order_id=" + str(order.id),
            metadata={"order_id": order.id},
        )

        return Response({"checkout_url": session.url})

class StrideWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        if sig_header is None:
            return Response({"error": "Missing signature"}, status=400)
        event = None


        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return Response(status=400)
        except stripe.SignatureVerificationError:
            return Response(status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            order_id = session["metadata"]["order_id"]
            order = Order.objects.get(id=order_id)
            order.status = "paid"
            order.save()

            tickets = order.tickets.all()
            for ticket in tickets:
                ticket.status = "booked"
                ticket.save()

        return Response(status=200)