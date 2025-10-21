from rest_framework.routers import DefaultRouter

from .views import MarcheViewSet

router = DefaultRouter()
router.register(r"marche", MarcheViewSet, basename="marche")

urlpatterns = router.urls
