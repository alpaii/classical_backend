import pytest
import pdb  # ✅ 디버거 추가
from ..models import Composer, Work
from .utils import create_api_test, list_api_test


@pytest.fixture
def test_data():
    composer_a = Composer.objects.create(
        name="Mozart", full_name="Wolfgang Amadeus Mozart"
    )
    composer_b = Composer.objects.create(
        name="Beethoven", full_name="Ludwig van Beethoven"
    )

    name_a = "Eine kleine Nachtmusik"
    name_b = "Symphony No.40"

    return {
        "normal": {
            "composer": composer_a.id,
            "work_no": "K.525",
            "name": name_a,
        },  # 정상 데이터
        "unique": {
            "composer": composer_a.id,
            "work_no": "K.525",
            "name": name_b,
        },  # composer & work_no 필드는 중복 불가
        "duplicate": {
            "composer": composer_b.id,
            "work_no": "K.525",
            "name": name_a,
        },  # composer가 다르면 work_no 필드는 중복 가능
        "expected": {
            "use_page": True,
            "cnt": 1,
            "field": "name",
            "value": name_a,
        },
    }


@pytest.mark.django_db
class TestWorkAPI:
    def test_create_work(self, api_client, test_data):
        create_api_test(api_client, Work, "work-list", test_data)

    def test_get_works(self, api_client, test_data):
        test_data["normal"]["composer"] = Composer.objects.get(
            id=test_data["normal"]["composer"]
        )
        Work.objects.create(**test_data["normal"])
        list_api_test(api_client, "work-list", test_data["expected"])
