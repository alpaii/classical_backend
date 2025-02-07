import pytest
import pdb  # ✅ 디버거 추가
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Performer


@pytest.mark.django_db
class TestPerformerAPI:
    def setup_method(self):
        self.client = APIClient()
        self.performer_data = {
            "name": "Yo-Yo",
            "full_name": "Yo-Yo Ma",
            "role": "Cello",
        }

    def test_create_performer(self):
        url = reverse("performer-list")
        response = self.client.post(url, self.performer_data, format="json")
        assert response.status_code == 201
        assert Performer.objects.count() == 1
        assert Performer.objects.first().name == "Yo-Yo"

    def test_get_performers(self):
        # pdb.set_trace()  # ✅ 여기서 디버깅 시작
        Performer.objects.create(**self.performer_data)
        url = reverse("performer-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
