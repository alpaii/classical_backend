import pytest
from ..models import Performer
from .utils import create_api_test, list_api_test  # ✅ 유틸리티 함수 임포트


@pytest.mark.django_db
class TestPerformerAPI:
    def setup_method(self):
        self.data = {
            "normal": {
                "name": "Yo-Yo",
                "full_name": "Yo-Yo Ma",
                "role": "Cello",
            },  # 정상 데이터
            "unique": {
                "name": "Yo-Yo",
                "full_name": "Another Yo-Yo Ma",
                "role": "Violin",
            },  # name 필드는 중복 불가
            "duplicate": {
                "name": "Yo-Yo Ma",
                "full_name": "Yo-Yo Ma",
                "role": "Cello",
            },  # full_name 필드는 중복 가능
        }

    def test_create_performer(self):
        create_api_test(Performer, "performer-list", self.data)

    def test_get_performers(self):
        list_api_test(Performer, "performer-list", self.data["normal"], use_page=True)
