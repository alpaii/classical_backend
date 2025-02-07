import pytest
from ..models import Composer
from .utils import create_api_test, list_api_test  # ✅ 유틸리티 함수 임포트


@pytest.mark.django_db
class TestComposerAPI:
    def setup_method(self):
        self.data = {
            "normal": {
                "name": "Beethoven",
                "full_name": "Ludwig van Beethoven",
            },  # 정상 데이터
            "unique": {
                "name": "Beethoven",
                "full_name": "Another van Beethoven",
            },  # name 필드는 중복 불가
            "duplicate": {
                "name": "Ceethoven",
                "full_name": "Ludwig van Beethoven",
            },  # full_name 필드는 중복 가능
        }

    def test_create_composer(self):
        create_api_test(Composer, "composer-list", self.data)

    def test_get_composers(self):
        list_api_test(Composer, "composer-list", self.data["normal"])
