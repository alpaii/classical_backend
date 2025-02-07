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
        performer_names = set()

        while len(performers) < 1000:
            last_name = fake.last_name()
            if last_name in performer_names:
                continue

            first_name = fake.first_name()
            full_name = f"{first_name} {last_name}"
            performer_names.add(last_name)

            performer = Performer(
                name=last_name,
                full_name=full_name,
                role=random.choice(ROLE_CHOICES),
            )
            performers.append(performer)

        Performer.objects.bulk_create(performers)  # 대량 삽입 최적화
        self.stdout.write(self.style.SUCCESS("Successfully generated 1000 performers"))
