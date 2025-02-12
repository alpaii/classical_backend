from rest_framework import serializers
from .models import Composer, Performer, Work, Recording, Cover, Album


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


class CoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cover
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class AlbumDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"
        depth = 3
