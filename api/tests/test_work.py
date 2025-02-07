import pytest
import pdb  # ✅ 디버거 추가
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Composer, Work


@pytest.mark.django_db
class TestWorkAPI:
    def setup_method(self):
        self.client = APIClient()
        self.composer = Composer.objects.create(
            name="Mozart", full_name="Wolfgang Amadeus Mozart"
        )
        self.work_data = {
            "composer": self.composer.id,
            "work_no": "K.525",
            "name": "Eine kleine Nachtmusik",
        }

    def test_create_work(self):
        url = reverse("work-list")
        response = self.client.post(url, self.work_data, format="json")
        assert response.status_code == 201
        assert Work.objects.count() == 1
        assert Work.objects.first().name == "Eine kleine Nachtmusik"

    def test_get_works(self):
        Work.objects.create(
            composer=self.composer, work_no="K.550", name="Symphony No.40"
        )
        url = reverse("work-list")
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 4
