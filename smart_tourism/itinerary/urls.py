from rest_framework.routers import DefaultRouter
from .views import CircuitViewSet, CircuitHistoryViewSet

router = DefaultRouter()
router.register(r'circuits', CircuitViewSet, basename='circuit')
router.register(r'circuit_history', CircuitHistoryViewSet, basename='circuit_history')


urlpatterns = router.urls
