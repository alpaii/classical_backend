import pytest
from ..models import Performer
from .utils import create_api_test, list_api_test


@pytest.fixture
def test_data():
    name_a = "Yo-Yo"
    name_b = "Another Yo-Yo"
    full_name_a = "Yo-Yo Ma"
    full_name_b = "Another Yo-Yo Ma"

    return {
        "normal": {
            "name": name_a,
            "full_name": full_name_a,
            "role": "Cello",
        },  # 정상 데이터
        "unique": {
            "name": name_a,
            "full_name": full_name_b,
            "role": "Cello",
        },  # name 필드는 중복 불가
        "duplicate": {
            "name": name_b,
            "full_name": full_name_a,
            "role": "Cello",
        },  # full_name 필드는 중복 가능
        "expected": {
            "use_page": True,
            "cnt": 1,
            "field": "name",
            "value": name_a,
        },
    }


@pytest.mark.django_db
class TestPerformerAPI:
    def test_create_performer(self, api_client, test_data):
        create_api_test(api_client, Performer, "performer-list", test_data)

    def test_get_performers(self, api_client, test_data):
        Performer.objects.create(**test_data["normal"])
        list_api_test(api_client, "performer-list", test_data["expected"])
