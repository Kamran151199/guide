from services.user.views.user import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register("", UserViewSet)

urlpatterns = router.urls
