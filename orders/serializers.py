from rest_framework import serializers
from .models import Order, Transaction

class OrderSerializer(serializers.ModelSerializer):
    seats = serializers.ListField(child=serializers.CharField(), write_only=True)
    flight = serializers.IntegerField(write_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'seats', 'flight', 'total_price', 'status']
        read_only_fields = ['total_price', 'status', 'user']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'order', 'user', 'status', 'transaction_id', 'amount', 'updated_at']