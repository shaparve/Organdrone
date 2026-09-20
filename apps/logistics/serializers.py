from rest_framework import serializers

from .models import Delivery, Drone, DroneLocation


class DroneLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DroneLocation
        fields = ('drone', 'latitude', 'longitude', 'updated_at')
        read_only_fields = ('updated_at', 'drone')


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('id', 'organ_request', 'organ', 'drone', 'status', 'assigned_at', 'delivered_at')


class DroneSerializer(serializers.ModelSerializer):
    location = DroneLocationSerializer(read_only=True)
    delivery = DeliverySerializer(read_only=True)

    class Meta:
        model = Drone
        fields = ('id', 'identifier', 'status', 'is_active', 'location', 'delivery')
        read_only_fields = ('status',)
