# tests/test_performer.py
import pytest, pdb
from django.urls import reverse
from ..models import Performer


@pytest.mark.django_db
class TestPerformerAPI:
    def setup_method(self):
        # pdb.set_trace()
        self.performers = {
            "Karajan": {
                "name": "Karajan",
                "full_name": "Herbert von Karajan",
                "role": "Conductor",
            },
            "Abbado": {
                "name": "Abbado",
                "full_name": "Claudio Abbado",
                "role": "Conductor",
            },
        }

    def test_post(self, api_client):
        test_data = {
            "normal": {
                "name": self.performers["Karajan"]["name"],
                "full_name": self.performers["Karajan"]["full_name"],
                "role": "Conductor",
            },  # 정상 데이터
            "unique": {
                "name": self.performers["Karajan"]["name"],
                "full_name": self.performers["Abbado"]["full_name"],
                "role": "Conductor",
            },  # name 필드는 중복 불가
            "duplicate": {
                "name": self.performers["Abbado"]["name"],
                "full_name": self.performers["Karajan"]["full_name"],
                "role": "Conductor",
            },  # full_name 필드는 중복 가능
        }
        url = reverse("performer-list")
        response = api_client.post(url, test_data["normal"], format="json")
        assert response.status_code == 201
        assert Performer.objects.count() == 1

        response = api_client.post(url, test_data["unique"], format="json")
        assert response.status_code == 400
        assert Performer.objects.count() == 1

        response = api_client.post(url, test_data["duplicate"], format="json")
        assert response.status_code == 201
        assert Performer.objects.count() == 2

    def test_get(self, api_client):
        Performer.objects.create(**self.performers["Karajan"])
        url = reverse("performer-list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == self.performers["Karajan"]["name"]

        # sort test
        Performer.objects.create(**self.performers["Abbado"])
        response = api_client.get(url)
        list = [item["name"] for item in response.data["results"]]
        assert list == sorted(list)

    def test_put(self, api_client):
        performer = Performer.objects.create(**self.performers["Karajan"])
        url = reverse("performer-detail", args=[performer.id])
        update_data = {
            "name": "UpdatedKarajan",
            "full_name": self.performers["Karajan"]["full_name"],
            "role": self.performers["Karajan"]["role"],
        }

        response = api_client.put(url, update_data, format="json")
        assert response.status_code == 200
        performer.refresh_from_db()
        assert performer.name == "UpdatedKarajan"

    def test_delete(self, api_client):
        performer = Performer.objects.create(**self.performers["Karajan"])
        url = reverse("performer-detail", args=[performer.id])

        response = api_client.delete(url)
        assert response.status_code == 204
        assert Performer.objects.count() == 0
