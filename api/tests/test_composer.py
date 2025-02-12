# tests/test_composer.py
import pytest, pdb
from django.urls import reverse
from ..models import Composer


@pytest.mark.django_db
class TestComposerAPI:
    def setup_method(self):
        # pdb.set_trace()
        self.composers = {
            "Beethoven": {
                "name": "Beethoven",
                "full_name": "Ludwig van Beethoven",
            },
            "Mozart": {
                "name": "Mozart",
                "full_name": "Wolfgang Amadeus Mozart",
            },
        }

    def test_post(self, api_client):
        test_data = {
            "normal": {
                "name": self.composers["Beethoven"]["name"],
                "full_name": self.composers["Beethoven"]["full_name"],
            },  # 정상 데이터
            "unique": {
                "name": self.composers["Beethoven"]["name"],
                "full_name": self.composers["Mozart"]["full_name"],
            },  # name 필드는 중복 불가
            "duplicate": {
                "name": self.composers["Mozart"]["name"],
                "full_name": self.composers["Beethoven"]["full_name"],
            },  # full_name 필드는 중복 가능
        }
        url = reverse("composer-list")

        response = api_client.post(url, test_data["normal"], format="json")
        assert response.status_code == 201
        assert Composer.objects.count() == 1

        response = api_client.post(url, test_data["unique"], format="json")
        assert response.status_code == 400
        assert Composer.objects.count() == 1

        response = api_client.post(url, test_data["duplicate"], format="json")
        assert response.status_code == 201
        assert Composer.objects.count() == 2

    def test_get(self, api_client):
        Composer.objects.create(**self.composers["Mozart"])
        url = reverse("composer-list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == self.composers["Mozart"]["name"]

        # sort test
        Composer.objects.create(**self.composers["Beethoven"])
        response = api_client.get(url)
        list = [item["name"] for item in response.data]
        assert list == sorted(list)

    def test_put(self, api_client):
        composer = Composer.objects.create(**self.composers["Mozart"])
        url = reverse("composer-detail", args=[composer.id])
        update_data = {"name": "UpdatedMozart", "full_name": "Wolfgang Amadeus Mozart"}

        response = api_client.put(url, update_data, format="json")
        assert response.status_code == 200
        composer.refresh_from_db()
        assert composer.name == "UpdatedMozart"

    def test_delete(self, api_client):
        composer = Composer.objects.create(**self.composers["Beethoven"])
        url = reverse("composer-detail", args=[composer.id])

        response = api_client.delete(url)
        assert response.status_code == 204
        assert Composer.objects.count() == 0
