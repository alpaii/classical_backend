from django.db import models


class Composer(models.Model):
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
