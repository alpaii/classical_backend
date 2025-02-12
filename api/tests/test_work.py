# tests/test_performer.py
import pytest, pdb
from django.urls import reverse
from ..models import Composer, Work


@pytest.mark.django_db
class TestWorkAPI:
    def setup_method(self):
        # pdb.set_trace()
        self.composers = {
            "Mozart": {
                "name": "Mozart",
                "full_name": "Wolfgang Amadeus Mozart",
            },
            "Beethoven": {
                "name": "Beethoven",
                "full_name": "Ludwig van Beethoven",
            },
        }
        self.composer_models = {
            "Mozart": Composer.objects.create(**self.composers["Mozart"]),
            "Beethoven": Composer.objects.create(**self.composers["Beethoven"]),
        }

        self.works = {
            "Beethoven Symphony No. 9": {
                "composer": self.composer_models["Beethoven"],
                "work_no": "Op. 125",
                "name": "Symphony No. 9 in D minor",
            },
            "Beethoven Symphony No. 7": {
                "composer": self.composer_models["Beethoven"],
                "work_no": "Op. _92",
                "name": "Symphony No. 7 in A major",
            },
            "Mozart Symphony No. 34": {
                "composer": self.composer_models["Mozart"],
                "work_no": "K. 338",
                "name": "Symphony No. 34 in C major",
            },
        }

    def test_post(self, api_client):
        test_data = {
            "normal": {
                "composer": self.works["Beethoven Symphony No. 9"]["composer"].id,
                "work_no": self.works["Beethoven Symphony No. 9"]["work_no"],
                "name": self.works["Beethoven Symphony No. 9"]["name"],
            },  # 정상 데이터
            "unique": {
                "composer": self.works["Beethoven Symphony No. 9"]["composer"].id,
                "work_no": self.works["Beethoven Symphony No. 9"]["work_no"],
                "name": self.works["Mozart Symphony No. 34"]["name"],
            },  # composer & work_no 필드는 중복 불가
            "duplicate": {
                "composer": self.works["Mozart Symphony No. 34"]["composer"].id,
                "work_no": self.works["Beethoven Symphony No. 9"]["work_no"],
                "name": self.works["Beethoven Symphony No. 9"]["name"],
            },  # composer가 다르면 work_no 필드는 중복 불가
        }
        url = reverse("work-list")
        response = api_client.post(url, test_data["normal"], format="json")
        assert response.status_code == 201
        assert Work.objects.count() == 1

        response = api_client.post(url, test_data["unique"], format="json")
        assert response.status_code == 400
        assert Work.objects.count() == 1

        response = api_client.post(url, test_data["duplicate"], format="json")
        assert response.status_code == 201
        assert Work.objects.count() == 2

    def test_get(self, api_client):
        Work.objects.create(**self.works["Beethoven Symphony No. 9"])
        url = reverse("work-list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert (
            response.data["results"][0]["name"]
            == self.works["Beethoven Symphony No. 9"]["name"]
        )

        # sort test
        Work.objects.create(**self.works["Mozart Symphony No. 34"])
        Work.objects.create(**self.works["Beethoven Symphony No. 7"])
        response = api_client.get(url)
        list = [item["name"] for item in response.data["results"]]
        assert list == [
            "Symphony No. 7 in A major",
            "Symphony No. 9 in D minor",
            "Symphony No. 34 in C major",
        ]

    def test_put(self, api_client):
        work = Work.objects.create(**self.works["Beethoven Symphony No. 9"])
        url = reverse("work-detail", args=[work.id])
        update_data = {
            "composer": self.works["Beethoven Symphony No. 9"]["composer"].id,
            "work_no": self.works["Beethoven Symphony No. 9"]["work_no"],
            "name": "Symphony No. 9",
        }

        response = api_client.put(url, update_data, format="json")
        assert response.status_code == 200
        work.refresh_from_db()
        assert work.name == "Symphony No. 9"

    def test_delete(self, api_client):
        work = Work.objects.create(**self.works["Beethoven Symphony No. 9"])
        url = reverse("work-detail", args=[work.id])

        response = api_client.delete(url)
        assert response.status_code == 204
        assert Work.objects.count() == 0
