from rest_framework.viewsets import ModelViewSet
from .models import Composer
from .serializers import (
    ComposerSerializer,
)


class ComposerViewSet(ModelViewSet):
    queryset = Composer.objects.all()
    serializer_class = ComposerSerializer
