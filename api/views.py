from rest_framework.viewsets import ModelViewSet
from .models import Composer, Performer
from .serializers import (
    ComposerSerializer,
    PerformerSerializer,
)


class ComposerViewSet(ModelViewSet):
    queryset = Composer.objects.all()
    serializer_class = ComposerSerializer


class PerformerViewSet(ModelViewSet):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer
    pagination_class = None  # ❌ 이 ViewSet에서는 페이지네이션을 사용하지 않음
