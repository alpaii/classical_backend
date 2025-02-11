# tests/utils.py
import pdb  # ✅ 디버거 추가
from django.urls import reverse


def create_api_test(api_client, model, url_name, data):
    """POST 요청을 보내어 객체를 생성하는 API 테스트 함수"""
    url = reverse(url_name)
    create_api_request(api_client, model, url, data["normal"], 201, 1)  # 정상
    create_api_request(api_client, model, url, data["unique"], 400, 1)  # 중복 불가
    create_api_request(api_client, model, url, data["duplicate"], 201, 2)  # 중복 가능


def list_api_test(api_client, url_name, expected_data):
    """GET 요청을 보내어 목록 API 테스트 함수"""
    url = reverse(url_name)
    response = api_client.get(url)
    assert response.status_code == 200

    # 페이지네이션을 사용 여부에 따라 결과 데이터 구조 다름
    res = response.data["results"] if expected_data["use_page"] else response.data
    assert len(res) == expected_data["cnt"]
    assert res[0][expected_data["field"]] == expected_data["value"]


def create_api_request(api_client, model, url, data, code, cnt):
    """POST 요청을 보내어 객체를 생성하는 API 요청 함수"""
    response = api_client.post(url, data, format="json")
    assert response.status_code == code
    assert model.objects.count() == cnt
