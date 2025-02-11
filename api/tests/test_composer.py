# tests/test_composer.py
import pytest
from ..models import Composer
from .utils import create_api_test, list_api_test


@pytest.fixture
def test_data():
    name_a = "Beethoven"
    name_b = "Mozart"
    full_name_a = "Ludwig van Beethoven"
    full_name_b = "Wolfgang Amadeus Mozart"

    return {
        "normal": {
            "name": name_a,
            "full_name": full_name_a,
        },  # 정상 데이터
        "unique": {
            "name": name_a,
            "full_name": full_name_b,
        },  # name 필드는 중복 불가
        "duplicate": {
            "name": name_b,
            "full_name": full_name_a,
        },  # full_name 필드는 중복 가능
        "expected": {
            "use_page": False,
            "cnt": 1,
            "field": "name",
            "value": name_a,
        },
    }


@pytest.mark.django_db
class TestComposerAPI:
    def test_create_composer(self, api_client, test_data):
        create_api_test(api_client, Composer, "composer-list", test_data)

    def test_get_composers(self, api_client, test_data):
        Composer.objects.create(**test_data["normal"])
        list_api_test(api_client, "composer-list", test_data["expected"])
