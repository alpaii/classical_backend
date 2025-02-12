# tests/test_performer.py
import pytest, pdb
from django.urls import reverse
from ..models import Performer, Composer, Work, Recording


@pytest.mark.django_db
class TestRecordingAPI:
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
        self.performer_models = {
            "Karajan": Performer.objects.create(**self.performers["Karajan"]),
            "Abbado": Performer.objects.create(**self.performers["Abbado"]),
        }

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
        self.work_models = {
            "Beethoven Symphony No. 9": Work.objects.create(
                **self.works["Beethoven Symphony No. 9"]
            ),
            "Beethoven Symphony No. 7": Work.objects.create(
                **self.works["Beethoven Symphony No. 7"]
            ),
            "Mozart Symphony No. 34": Work.objects.create(
                **self.works["Mozart Symphony No. 34"]
            ),
        }

        self.recordings = {
            "(1962) Beethoven Symphony No. 9 - Karajan": {
                "work": self.work_models["Beethoven Symphony No. 9"],
                "performers": [self.performer_models["Karajan"]],
                "year": 1962,
                "name": "(1962) Beethoven Symphony No. 9 - Karajan",
            },
            "(1977) Beethoven Symphony No. 7 - Karajan": {
                "work": self.work_models["Beethoven Symphony No. 7"],
                "performers": [self.performer_models["Karajan"]],
                "year": 1977,
                "name": "(1977) Beethoven Symphony No. 7 - Karajan",
            },
            "(1968) Mozart Symphony No. 34 - Abbado": {
                "work": self.work_models["Mozart Symphony No. 34"],
                "performers": [self.performer_models["Abbado"]],
                "year": 1968,
                "name": "(1968) Mozart Symphony No. 34 - Abbado",
            },
        }

    def test_post(self, api_client):
        test_data = {
            "normal": {
                "work": self.recordings["(1962) Beethoven Symphony No. 9 - Karajan"][
                    "work"
                ].id,
                "performers": [
                    self.recordings["(1962) Beethoven Symphony No. 9 - Karajan"][
                        "performers"
                    ][0].id
                ],
                "year": self.recordings["(1962) Beethoven Symphony No. 9 - Karajan"][
                    "year"
                ],
                "name": self.recordings["(1962) Beethoven Symphony No. 9 - Karajan"][
                    "name"
                ],
            },  # 정상 데이터
            "unique": {
                "work": self.recordings["(1977) Beethoven Symphony No. 7 - Karajan"][
                    "work"
                ].id,
                "performers": [
                    self.recordings["(1977) Beethoven Symphony No. 7 - Karajan"][
                        "performers"
                    ][0].id
                ],
                "year": self.recordings["(1977) Beethoven Symphony No. 7 - Karajan"][
                    "year"
                ],
                "name": self.recordings["(1962) Beethoven Symphony No. 9 - Karajan"][
                    "name"
                ],
            },  # name 필드는 중복 불가
            "duplicate": {
                "work": self.recordings["(1962) Beethoven Symphony No. 9 - Karajan"][
                    "work"
                ].id,
                "performers": [
                    self.recordings["(1962) Beethoven Symphony No. 9 - Karajan"][
                        "performers"
                    ][0].id
                ],
                "year": self.recordings["(1962) Beethoven Symphony No. 9 - Karajan"][
                    "year"
                ],
                "name": self.recordings["(1977) Beethoven Symphony No. 7 - Karajan"][
                    "name"
                ],
            },  # name 필드가 다르면 중복 가능
        }
        url = reverse("recording-list")
        response = api_client.post(url, test_data["normal"], format="json")
        assert response.status_code == 201
        assert Recording.objects.count() == 1

        response = api_client.post(url, test_data["unique"], format="json")
        assert response.status_code == 400
        assert Recording.objects.count() == 1

        response = api_client.post(url, test_data["duplicate"], format="json")
        assert response.status_code == 201
        assert Recording.objects.count() == 2

    def test_get(self, api_client):
        recording_data = self.recordings["(1977) Beethoven Symphony No. 7 - Karajan"]
        performers = recording_data.pop("performers")
        recording = Recording.objects.create(**recording_data)
        recording.performers.set(performers)  # ManyToMany 관계 설정

        url = reverse("recording-list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert (
            response.data["results"][0]["name"]
            == self.recordings["(1977) Beethoven Symphony No. 7 - Karajan"]["name"]
        )

        # sort test
        recording_data = self.recordings["(1962) Beethoven Symphony No. 9 - Karajan"]
        performers = recording_data.pop("performers")
        recording = Recording.objects.create(**recording_data)
        recording.performers.set(performers)  # ManyToMany 관계 설정

        response = api_client.get(url)
        list = [item["name"] for item in response.data["results"]]
        assert list == [
            "(1962) Beethoven Symphony No. 9 - Karajan",
            "(1977) Beethoven Symphony No. 7 - Karajan",
        ]

    def test_put(self, api_client):
        recording_data = self.recordings["(1962) Beethoven Symphony No. 9 - Karajan"]
        performers = recording_data.pop("performers")
        recording = Recording.objects.create(**recording_data)
        recording.performers.set(performers)  # ManyToMany 관계 설정

        url = reverse("recording-detail", args=[recording.id])
        update_data = {
            "work": recording.work.id,
            "performers": [performers[0].id],
            "year": 1970,
            "name": "(1970) Beethoven Symphony No. 9 - Karajan",
        }

        response = api_client.put(url, update_data, format="json")
        assert response.status_code == 200
        recording.refresh_from_db()
        assert recording.name == "(1970) Beethoven Symphony No. 9 - Karajan"

    def test_delete(self, api_client):
        recording_data = self.recordings["(1962) Beethoven Symphony No. 9 - Karajan"]
        performers = recording_data.pop("performers")
        recording = Recording.objects.create(**recording_data)
        recording.performers.set(performers)  # ManyToMany 관계 설정

        url = reverse("recording-detail", args=[recording.id])
        response = api_client.delete(url)
        assert response.status_code == 204
        assert Recording.objects.count() == 0
