from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import (
    BuildingViewSet,
    UserViewSet,
    SmartDeviceViewSet,
    ReadingViewSet,
    BuildingInchargeViewSet,
    SmartDeviceReadingViewSet,
    RegisterView,
)

# Create a Default Router
router = DefaultRouter()
router.register(r'buildings', BuildingViewSet)
router.register(r'users', UserViewSet)
router.register(r'smartdevices', SmartDeviceViewSet, basename='smartdevice')
router.register(r'readings', ReadingViewSet, basename='reading')
router.register(r'buildingincharges', BuildingInchargeViewSet)

# Create a Nested Router for SmartDevice readings
smartdevice_router = NestedDefaultRouter(router, r'smartdevices', lookup='smartdevice')
smartdevice_router.register(r'readings', SmartDeviceReadingViewSet, basename='smartdevice-readings')

# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),             # Include main router URLs
    path('', include(smartdevice_router.urls)), # Include nested router URLs
    path('register/', RegisterView.as_view(), name='register'), # User registration endpoint
]
