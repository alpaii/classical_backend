import pytest
import pdb  # ✅ 디버거 추가
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Composer


@pytest.mark.django_db
class TestComposerAPI:
    def setup_method(self):
        self.client = APIClient()
        self.composer_data = {"name": "Beethoven", "full_name": "Ludwig van Beethoven"}

    def test_create_composer(self):
        url = reverse("composer-list")  # DRF ViewSet 엔드포인트
        response = self.client.post(url, self.composer_data, format="json")
        assert response.status_code == 201
        assert Composer.objects.count() == 1
        assert Composer.objects.first().name == "Beethoven"

    def test_get_composers(self):
        Composer.objects.create(**self.composer_data)
        url = reverse("composer-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
