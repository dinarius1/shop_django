from rest_framework.serializers import ModelSerializer
from drf_writable_nested import  WritableNestedModelSerializer

from .models import Order, OrderItems

class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItems
        exclude = ('order',)

class OrderSerializer(WritableNestedModelSerializer, ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ('user', 'is_paid', 'created_at', 'total_price', 'items')
