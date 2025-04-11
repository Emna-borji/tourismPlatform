from django.shortcuts import render

from rest_framework import viewsets
from .models import Circuit
from .serializers import CircuitCreateSerializer
from users.permissions import CircuitPermission  # import the new one
from .models import CircuitHistory
from .serializers import CircuitHistorySerializer
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status





class CircuitViewSet(viewsets.ModelViewSet):
    queryset = Circuit.objects.all()
    serializer_class = CircuitCreateSerializer
    permission_classes = [CircuitPermission]  # ✅ add it here



class CircuitHistoryViewSet(viewsets.ModelViewSet):
    queryset = CircuitHistory.objects.all()
    serializer_class = CircuitHistorySerializer

    def create(self, request, *args, **kwargs):
        # Retrieve the data from the request
        circuit_id = request.data.get('circuit')
        departure_date = request.data.get('departure_date')
        arrival_date = request.data.get('arrival_date')

        # Parse the dates
        try:
            departure_date = datetime.strptime(departure_date, "%Y-%m-%d")
            arrival_date = datetime.strptime(arrival_date, "%Y-%m-%d")
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the duration in days
        delta = arrival_date - departure_date
        duration_in_days = delta.days

        # Fetch the circuit to compare the duration
        try:
            circuit = Circuit.objects.get(id=circuit_id)
        except Circuit.DoesNotExist:
            return Response({"error": "Circuit not found."}, status=status.HTTP_404_NOT_FOUND)

        # Compare the duration with the circuit's duration
        if duration_in_days != circuit.duration:
            return Response(
                {"error": f"The duration of the circuit must be {circuit.duration} days."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If everything is valid, proceed with the creation of the CircuitHistory
        return super().create(request, *args, **kwargs)
