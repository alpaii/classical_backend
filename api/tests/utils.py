# tests/utils.py
import pdb  # ✅ 디버거 추가
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import Composer


def test_post_api(data):
    api_client = APIClient()

    url = reverse("composer-list")
    test_model = Composer
    request_post(api_client, test_model, url, data["normal"], 201, 1)  # 정상
    request_post(api_client, test_model, url, data["unique"], 400, 1)  # 중복 불가
    request_post(api_client, test_model, url, data["duplicate"], 201, 2)  # 중복 가능


def request_post(api_client, model, url, data, code, cnt):
    response = api_client.post(url, data, format="json")
    assert response.status_code == code
    assert model.objects.count() == cnt


# def test_get_api(api_client, url_name, expected_data):
#     url = reverse(url_name)
#     response = api_client.get(url)
#     assert response.status_code == 200

#     # 페이지네이션을 사용 여부에 따라 결과 데이터 구조 다름
#     res = response.data["results"] if expected_data["use_page"] else response.data
#     assert len(res) == expected_data["cnt"]
#     assert res[0][expected_data["field"]] == expected_data["value"]


# def test_get_sort(api_client, url_name, expected_data):
#     url = reverse(url_name)
#     response = api_client.get(url)
#     assert response.status_code == 200

#     # 페이지네이션을 사용 여부에 따라 결과 데이터 구조 다름
#     res = response.data["results"] if expected_data["use_page"] else response.data
#     res_list = [item[expected_data["field"]] for item in res]
#     assert res_list == sorted(res_list)
