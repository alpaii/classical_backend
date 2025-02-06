from django.db import models


class Performer(models.Model):
    ROLE_CHOICES = [
        ("Conductor", "Conductor"),
        ("Orchestra", "Orchestra"),
        ("Ensemble", "Ensemble"),
        ("Choir", "Choir"),
        ("Piano", "Piano"),
        ("Violin", "Violin"),
        ("Cello", "Cello"),
        ("Viola", "Viola"),
        ("Double Bass", "Double Bass"),
        ("Flute", "Flute"),
    ]

    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


class Composer(models.Model):
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Work(models.Model):
    composer = models.ForeignKey(Composer, on_delete=models.CASCADE)
    work_no = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["composer", "work_no"], name="unique_composer_work_no"
            )
        ]

    def __str__(self):
        return f"{self.composer.name} ({self.work_no}) {self.name}"
