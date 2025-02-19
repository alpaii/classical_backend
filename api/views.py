from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
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

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get("search", None)

        if search_query:
            queryset = queryset.filter(full_name__icontains=search_query)

        return queryset


class PerformerViewSet(ModelViewSet):
    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get("search", None)
        role_query = self.request.query_params.get("role", None)

        if search_query:
            queryset = queryset.filter(full_name__icontains=search_query)
        if role_query:
            queryset = queryset.filter(role=role_query)

        return queryset


class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    def filter_queryset(self, queryset):
        composer_id = self.request.query_params.get("composer")
        if composer_id:
            queryset = queryset.filter(composer_id=composer_id)

        search_query = self.request.query_params.get("search")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    @action(detail=False, methods=["post"])
    def bulk_create(self, request):
        serializer = WorkSerializer(data=request.data, many=True)  # ✅ 다중 데이터 처리
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkDetailViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkDetailSerializer


class RecordingViewSet(ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

    def filter_queryset(self, queryset):
        work_id = self.request.query_params.get("work")  # GET 요청에서 work ID 가져오기
        if work_id:
            queryset = queryset.filter(work_id=work_id)  # 특정 Composer의 Work 필터링
        return queryset


class RecordingDetailViewSet(ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingDetailSerializer

    def filter_queryset(self, queryset):
        work_id = self.request.query_params.get("work")  # GET 요청에서 work ID 가져오기
        if work_id:
            queryset = queryset.filter(work_id=work_id)  # 특정 Composer의 Work 필터링
        return queryset


class CoverViewSet(ModelViewSet):
    queryset = Cover.objects.all()
    serializer_class = CoverSerializer


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class AlbumDetailViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumDetailSerializer
