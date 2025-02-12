from rest_framework import serializers
from .models import Composer, Performer, Work, Recording


class ComposerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composer
        fields = "__all__"


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        fields = "__all__"


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"


class WorkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"
        depth = 1


class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = "__all__"


class RecordingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = "__all__"
        depth = 2
