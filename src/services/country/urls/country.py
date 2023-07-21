from rest_framework.routers import DefaultRouter
from services.country.views.country import CountryViewSet

router = DefaultRouter()
router.register('', CountryViewSet, basename="countries")

urlpatterns = router.urls
