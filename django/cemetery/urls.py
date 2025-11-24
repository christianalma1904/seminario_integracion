from rest_framework.routers import DefaultRouter
from .views import SectorViewSet, GraveViewSet, DeceasedViewSet

router = DefaultRouter()
router.register("sectors", SectorViewSet, basename="sector")
router.register("graves", GraveViewSet, basename="grave")
router.register("deceased", DeceasedViewSet, basename="deceased")

urlpatterns = router.urls
