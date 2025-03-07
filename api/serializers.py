from rest_framework import serializers
from .models import Composer, Performer, Work, Recording, Cover, Album


class ComposerSerializer(serializers.ModelSerializer):
    work_count = serializers.IntegerField(read_only=True)  # ✅ 추가 필드

    class Meta:
        model = Composer
        fields = ["id", "name", "full_name", "work_count"]  # ✅ work_count 포함


class PerformerSerializer(serializers.ModelSerializer):
    recording_count = serializers.IntegerField(read_only=True)  # ✅ 추가 필드

    class Meta:
        model = Performer
        fields = [
            "id",
            "name",
            "full_name",
            "role",
            "recording_count",
        ]  # ✅ recording_count 포함


class WorkSerializer(serializers.ModelSerializer):
    recording_count = serializers.IntegerField(read_only=True)  # ✅ 추가 필드

    class Meta:
        model = Work
        fields = [
            "id",
            "composer",
            "work_no",
            "name",
            "recording_count",
        ]  # ✅ recording_count 포함


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
