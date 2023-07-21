from rest_framework.routers import DefaultRouter
from services.country.views.domain import DomainViewSet

router = DefaultRouter()
router.register(r"domains", DomainViewSet, basename="domains")

urlpatterns = router.urls
