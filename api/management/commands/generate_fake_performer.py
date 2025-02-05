import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import Performer

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake performer data"

    def handle(self, *args, **kwargs):
        ROLE_CHOICES = [
            "Conductor",
            "Orchestra",
            "Ensemble",
            "Choir",
            "Piano",
            "Violin",
            "Cello",
            "Viola",
            "Double Bass",
            "Flute",
        ]

        performers = []
        for _ in range(1000):  # 1000개의 데이터 생성
            performer = Performer(
                name=fake.last_name(),
                full_name=fake.name(),
                role=random.choice(ROLE_CHOICES),
            )
            performers.append(performer)

        Performer.objects.bulk_create(performers)  # 대량 삽입 최적화
        self.stdout.write(self.style.SUCCESS("Successfully generated 1000 performers"))
