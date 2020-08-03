from rest_framework import serializers
from src.co2_consumption.models import Consumption


class ConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumption
        fields = (
            'datetime',
            'co2_rate',
        )
