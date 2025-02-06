import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import Work, Composer

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake work data without duplicate composer-work_no pairs"

    def handle(self, *args, **kwargs):
        composers = list(Composer.objects.all())
        works = []
        created_count = 0
        target_count = 1000  # 목표 개수

        while created_count < target_count:
            composer = random.choice(composers)
            num = random.randint(1, 199)
            work_no = f"Op. {'_' * (3 - len(str(num)))}{num}"  # 빈 자리 `_`로 채움

            # 중복 검사: 같은 composer + work_no 조합이 존재하는지 확인
            if not Work.objects.filter(composer=composer, work_no=work_no).exists():
                work = Work(
                    composer=composer, work_no=work_no, name=fake.sentence(nb_words=3)
                )
                works.append(work)
                created_count += 1  # 성공적으로 추가된 경우만 카운트 증가

            # bulk_create를 사용해 100개씩 배치 삽입 (메모리 절약 및 최적화)
            if len(works) >= 100:
                Work.objects.bulk_create(works)
                works = []  # 리스트 초기화

        # 남아있는 데이터가 있다면 마지막으로 삽입
        if works:
            Work.objects.bulk_create(works)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully generated {target_count} unique works")
        )
