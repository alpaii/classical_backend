from rest_framework.viewsets import ModelViewSet
from .models import Composer, Performer, Work, Recording
from .serializers import (
    ComposerSerializer,
    PerformerSerializer,
    WorkSerializer,
    WorkDetailSerializer,
    RecordingSerializer,
    RecordingDetailSerializer,
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
