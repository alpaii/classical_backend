from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count

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
    queryset = Composer.objects.annotate(work_count=Count("work"))  # ✅ work 개수 추가
    serializer_class = ComposerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get("search", None)

        if search_query:
            queryset = queryset.filter(full_name__icontains=search_query)

        return queryset.order_by("name")  # ✅ 정렬 추가

    # ✅ Bulk Insert 지원 추가
    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):  # 요청이 리스트인지 확인
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PerformerViewSet(ModelViewSet):
    queryset = Performer.objects.annotate(
        recording_count=Count("recording")
    )  # ✅ recording 개수 추가
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
    queryset = Work.objects.annotate(
        recording_count=Count("recording")
    )  # ✅ recording 개수 추가
    serializer_class = WorkSerializer

    def filter_queryset(self, queryset):
        composer_id = self.request.query_params.get("composer")
        if composer_id:
            queryset = queryset.filter(composer_id=composer_id)

        search_work_no = self.request.query_params.get("search_work_no")
        if search_work_no:
            queryset = queryset.filter(work_no__icontains=search_work_no)

        search_name = self.request.query_params.get("search_name")
        if search_name:
            queryset = queryset.filter(name__icontains=search_name)

        return queryset.order_by("composer", "work_no")

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
