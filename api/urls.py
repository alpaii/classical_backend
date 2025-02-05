from rest_framework.routers import DefaultRouter
from .views import (
    ComposerViewSet,
)

router = DefaultRouter()
router.register(r"composers", ComposerViewSet, basename="composer")

urlpatterns = router.urls
