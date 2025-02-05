from rest_framework import serializers
from .models import Composer, Performer


class ComposerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composer
        fields = "__all__"


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        fields = "__all__"
