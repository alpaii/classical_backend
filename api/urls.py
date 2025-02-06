from rest_framework.routers import DefaultRouter
from .views import (
    ComposerViewSet,
    PerformerViewSet,
    WorkViewSet,
)

router = DefaultRouter()
router.register(r"composers", ComposerViewSet, basename="composer")
router.register(r"performers", PerformerViewSet, basename="performer")
router.register(r"works", WorkViewSet, basename="work")

urlpatterns = router.urls
