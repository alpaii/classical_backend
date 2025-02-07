import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import Composer

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake composer data"

    def handle(self, *args, **kwargs):
        composers = []
        composer_names = set()

        while len(composers) < 1000:
            last_name = fake.last_name()
            if last_name in composer_names:
                continue  # 중복 방지

            first_name = fake.first_name()
            full_name = f"{first_name} {last_name}"  # ✅ 이름을 일치시키도록 수정
            composer_names.add(last_name)

            composer = Composer(
                name=last_name,  # ✅ 성만 저장
                full_name=full_name,  # ✅ full_name은 "이름 성" 형태
            )
            composers.append(composer)

        Composer.objects.bulk_create(composers)  # 대량 삽입 최적화
        self.stdout.write(
            self.style.SUCCESS(f"Successfully generated {len(composers)} composers")
        )
