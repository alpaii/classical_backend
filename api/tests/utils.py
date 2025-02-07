# tests/utils.py  ✅ 유틸리티 함수 분리
import pytest
import pdb  # ✅ 디버거 추가
from rest_framework.test import APIClient
from django.urls import reverse


def create_api_test(model, url_name, data):
    """POST 요청을 보내어 객체를 생성하는 API 테스트 함수"""
    url = reverse(url_name)
    response = APIClient().post(url, data["normal"], format="json")
    assert response.status_code == 201
    assert model.objects.count() == 1

    # 중복 불가 데이터로 POST 요청을 보내면 400 에러가 발생해야 합니다.
    response = APIClient().post(url, data["unique"], format="json")
    assert response.status_code == 400

    # 중복 허용 데이터로 POST 요청을 보내면 객체가 생성되어야 합니다.
    response = APIClient().post(url, data["duplicate"], format="json")
    assert response.status_code == 201


def list_api_test(model, url_name, data):
    """GET 요청을 보내어 목록 API 테스트 함수"""
    model.objects.create(**data)
    url = reverse(url_name)
    response = APIClient().get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
