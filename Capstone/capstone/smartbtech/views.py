from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Building, Users, SmartDevice, Reading, BuildingIncharge
from django.utils.dateparse import parse_datetime
from .serializers import (
    BuildingSerializer,
    UserSerializer,
    SmartDeviceSerializer,
    ReadingSerializer,
    BuildingInchargeSerializer
)
from rest_framework.exceptions import NotFound


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class SmartDeviceViewSet(viewsets.ModelViewSet):
    queryset = SmartDevice.objects.all()
    serializer_class = SmartDeviceSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

class SmartDeviceReadingViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingSerializer

    def get_queryset(self):
        # Get the smart device ID from the URL kwargs
        smartdevice_id = self.kwargs.get('smartdevice_pk')

        # Validate the existence of the smart device
        try:
            device = SmartDevice.objects.get(pk=smartdevice_id)
        except SmartDevice.DoesNotExist:
            raise NotFound(detail=f"Smart device with ID {smartdevice_id} not found.")

        queryset = Reading.objects.filter(device=device)

        # Get start and end parameters from the request
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)

        # Parse the timestamps
        if start:
            start = parse_datetime(start)
        if end:
            end = parse_datetime(end)

        # Apply filtering logic
        if start and end:
            queryset = queryset.filter(reading_timestamp__range=(start, end))
        elif start:
            queryset = queryset.filter(reading_timestamp__gte=start)
        elif end:
            queryset = queryset.filter(reading_timestamp__lte=end)

        return queryset

class ReadingViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingSerializer

    def get_queryset(self):
        queryset = Reading.objects.all()

        # Get start and end parameters from the request
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)

        # Parse the timestamps
        if start:
            start = parse_datetime(start)
        if end:
            end = parse_datetime(end)

        # Apply filtering logic
        if start and end:
            queryset = queryset.filter(reading_timestamp__range=(start, end))
        elif start:
            queryset = queryset.filter(reading_timestamp__gte=start)
        elif end:
            queryset = queryset.filter(reading_timestamp__lte=end)

        return queryset



class BuildingInchargeViewSet(viewsets.ModelViewSet):
    queryset = BuildingIncharge.objects.all()
    serializer_class = BuildingInchargeSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
