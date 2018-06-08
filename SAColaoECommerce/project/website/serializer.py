from rest_framework import serializers
from . import models


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = (
            'user',
            'cpf',
        )
        model = models.Client

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = (
            'order_id',
            'user',
            'date_of_order',
            'date_of_payment',
            'price'
        )
        model = models.Order

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = (
            'order',
            'name',
            'brand',
            'description',
            'price',
            'amount',
            'category'
        )
        model = models.Product