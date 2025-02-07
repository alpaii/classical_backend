from rest_framework.viewsets import ModelViewSet
from .models import Composer, Performer, Work
from .serializers import (
    ComposerSerializer,
    PerformerSerializer,
    WorkSerializer,
    WorkDetailSerializer,
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
