from .models import Order, Transaction
from .serializers import OrderSerializer, TransactionSerializer
import logging
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
import stripe
from airport_project.permissions import IsOwnerOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Response
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from flights.models import Seat, Ticket
import os
from django.conf import settings
import time
from orders.utils import send_ticket_email
from django.http import HttpResponse

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
        seats = request.data.get("seats")
        flight_id = request.data.get("flight")

        if not seats:
            raise ValidationError("Seats are required.")

        if not flight_id:
            raise ValidationError("Flight is required.")

        order = Order.objects.create(
            user=request.user,
            total_price=0
        )

        total = 0

        for seat_number in seats:
            try:
                seat = Seat.objects.get(flight_id=flight_id, seat_number=seat_number)
            except Seat.DoesNotExist:
                order.delete()
                raise ValidationError(f"Seat {seat_number} does not exist")

            if not seat.is_available:
                order.delete()
                raise ValidationError(f"Seat {seat_number} is already booked")

            seat.is_available = False
            seat.save()

            ticket = Ticket.objects.create(
                user=request.user,
                flight_id=flight_id,
                order=order,
                seat_number=seat_number,
                price=seat.flight.price,
                status=Ticket.Status.BOOKED
            )

            total += ticket.price

        order.total_price = total
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

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
        order_id = request.data.get("order_id")

        if not order_id:
            return Response({"error": "order_id is required"}, status=400)

        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if order.status != "pending":
            return Response({"error": "Order is not pending"}, status=400)

        tickets = order.tickets.all()

        if not tickets.exists():
            return Response({"error": "Order has no tickets"}, status=400)

        flight = tickets[0].flight


        DOMAIN = os.getenv("DOMAIN", "http://localhost:8000")

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": f"Flight {flight.id}"},
                        "unit_amount": int(flight.price * 100),
                    },
                    "quantity": len(tickets),
                }
            ],
            mode="payment",
            success_url=DOMAIN + "stripe/webhook/success?order_id=" + str(order.id),
            cancel_url=DOMAIN + "stripe/webhook/cancel?order_id=" + str(order.id),
            metadata={"order_id": order.id},
            expires_at=int(time.time()) + 1800
        )

        Transaction.objects.create(
            order=order,
            user=user,
            status=Transaction.Status.PENDING,
            transaction_id=session.id,
            amount=order.total_price
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
        except ValueError as e:
            logger.error(f"Value error {e}")
            return Response(status=200)
        except stripe.SignatureVerificationError as e:
            logger.error(f"Signature error {e}")
            return Response(status=200)
        
        session = event['data']['object']
        order_id = session['metadata']['order_id']
        order = Order.objects.get(id=order_id)
        transaction = Transaction.objects.get(transaction_id=session.id)
        if transaction.status == transaction.Status.SUCCESS:
            logger.info(f"Already succesful transaction with id={transaction.id}")
            return Response(status=200)
        
        tickets = order.tickets.all()
        flight = tickets[0].flight

        if event["type"] == "checkout.session.completed":
            transaction.status = Transaction.Status.SUCCESS
            transaction.save()
            order.status = "paid"
            order.save()
            
            send_ticket_email(order, tickets)

            for ticket in tickets:
                ticket.status = "booked"
                ticket.save()

        elif event['type'] == 'checkout.session.expired':
            transaction.status = Transaction.Status.FAILED
            transaction.save()
            order.status = 'expired'
            order.save()

            for ticket in tickets:
                ticket.status = "cancelled"
                ticket.save()
                
            seat_numbers = [ticket.seat_number for ticket in tickets]
            seats = Seat.objects.filter(flight=flight, seat_number__in=seat_numbers)
            
            for seat in seats:
                seat.is_available = True
                seat.save()
                
        return Response(status=200)
    

def payment_success(request):
    order_id = request.GET.get('order_id')
    return HttpResponse(f"Оплата успішна! Order ID: {order_id}")

def payment_cancel(request):
    order_id = request.GET.get('order_id')
    return HttpResponse(f"Оплата скасована. Order ID: {order_id}")