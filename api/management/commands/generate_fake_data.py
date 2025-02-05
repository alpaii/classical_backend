import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import Composer

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake composer data"

    def handle(self, *args, **kwargs):
        composers = []
        for _ in range(1000):  # 1000개의 데이터 생성
            composer = Composer(
                name=fake.last_name(),
                full_name=fake.name(),
            )
            composers.append(composer)

        Composer.objects.bulk_create(composers)  # 대량 삽입 최적화
        self.stdout.write(self.style.SUCCESS("Successfully generated 1000 composers"))
