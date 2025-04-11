from rest_framework import serializers
from .models import Circuit, CircuitSchedule
from .models import CircuitHistory



class CircuitScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitSchedule
        exclude = ['circuit']  # Don't include 'circuit' in the request payload



class CircuitCreateSerializer(serializers.ModelSerializer):
    schedules = CircuitScheduleSerializer(many=True, required=False)

    class Meta:
        model = Circuit
        fields = '__all__'  # Or explicitly: ['name', 'circuit_code', 'departure_city', 'arrival_city', 'price', 'duration', 'description', 'schedules']

    def validate(self, data):
        if data['departure_city'] == data['arrival_city']:
            raise serializers.ValidationError("La ville de départ et d'arrivée doivent être différentes.")
        return data

    def create(self, validated_data):
        schedules_data = validated_data.pop('schedules', [])
        circuit = Circuit.objects.create(**validated_data)
        for schedule in schedules_data:
            CircuitSchedule.objects.create(circuit=circuit, **schedule)
        return circuit



class CircuitHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitHistory
        fields = ['id', 'circuit', 'departure_date', 'arrival_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']  # These fields should not be updated via the API