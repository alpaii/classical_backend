import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import Recording, Work, Performer


class Command(BaseCommand):
    help = "Generate fake recordings"

    def handle(self, *args, **kwargs):
        fake = Faker()
        works = list(Work.objects.all())
        performers = list(Performer.objects.all())

        if not works or not performers:
            self.stdout.write(
                self.style.ERROR("먼저 Work 및 Performer 모델에 데이터를 추가하세요.")
            )
            return

        for _ in range(1000):  # 10개의 Recording 생성
            work = random.choice(works)
            year = fake.year()
            name = fake.sentence(nb_words=4)

            recording = Recording.objects.create(work=work, year=year, name=name)

            # Performers 랜덤 추가
            num_performers = random.randint(1, 5)
            selected_performers = random.sample(performers, num_performers)
            recording.performers.set(selected_performers)

            self.stdout.write(
                self.style.SUCCESS(
                    f"생성된 Recording: {recording.name} ({recording.year})"
                )
            )
