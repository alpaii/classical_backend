# tests/test_composer.py
import pytest
from ..models import Composer
from .utils import test_post_api  # , test_get_api, test_get_sort


@pytest.mark.django_db
class TestComposerAPI:
    def test_post(self):
        test_data = {
            "normal": {
                "name": "Beethoven",
                "full_name": "Ludwig van Beethoven",
            },  # 정상 데이터
            "unique": {
                "name": "Beethoven",
                "full_name": "Wolfgang Amadeus Mozart",
            },  # name 필드는 중복 불가
            "duplicate": {
                "name": "Mozart",
                "full_name": "Ludwig van Beethoven",
            },  # full_name 필드는 중복 가능
        }
        test_post_api(test_data)
        # test_post_api(api_client, Composer, "composer-list", test_data)

    # def test_get(self, api_client):
    #     Composer.objects.create(name="Mozart", full_name="Wolfgang Amadeus Mozart")
    #     expected_data = {
    #         "use_page": False,
    #         "cnt": 1,
    #         "field": "name",
    #         "value": "Mozart",
    #     }
    #     test_get_api(api_client, "composer-list", expected_data)

    #     Composer.objects.create(name="Beethoven", full_name="Ludwig van Beethoven")
    #     test_get_sort(api_client, "composer-list", expected_data)
