import pytest
import pdb  # ✅ 디버거 추가
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Composer, Performer, Work


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
