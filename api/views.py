from rest_framework.viewsets import ModelViewSet
from .models import Composer, Performer, Work, Recording, Cover, Album
from .serializers import (
    ComposerSerializer,
    PerformerSerializer,
    WorkSerializer,
    WorkDetailSerializer,
    RecordingSerializer,
    RecordingDetailSerializer,
    CoverSerializer,
    AlbumSerializer,
    AlbumDetailSerializer,
)


class ComposerViewSet(ModelViewSet):
    queryset = Composer.objects.all()
    serializer_class = ComposerSerializer
    pagination_class = None


class PerformerViewSet(ModelViewSet):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer


class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class WorkDetailViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkDetailSerializer


class RecordingViewSet(ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer


class RecordingDetailViewSet(ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingDetailSerializer


class CoverViewSet(ModelViewSet):
    queryset = Cover.objects.all()
    serializer_class = CoverSerializer


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class AlbumDetailViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumDetailSerializer
