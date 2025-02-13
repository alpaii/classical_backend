from rest_framework.routers import DefaultRouter
from .views import (
    ComposerViewSet,
    PerformerViewSet,
    WorkViewSet,
    WorkDetailViewSet,
    RecordingViewSet,
    RecordingDetailViewSet,
    CoverViewSet,
    AlbumViewSet,
    AlbumDetailViewSet,
)

router = DefaultRouter()
router.register(r"composers", ComposerViewSet, basename="composer")
router.register(r"performers", PerformerViewSet, basename="performer")
router.register(r"works", WorkViewSet, basename="work")
router.register(r"work-details", WorkDetailViewSet, basename="work-detail")
router.register(r"recordings", RecordingViewSet, basename="recording")
router.register(
    r"recording-details", RecordingDetailViewSet, basename="recording-detail"
)
router.register(r"covers", CoverViewSet, basename="cover")
router.register(r"albums", AlbumViewSet, basename="album")
router.register(r"album-details", AlbumDetailViewSet, basename="album-detail")

urlpatterns = router.urls
