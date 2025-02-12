# Generated by Django 5.1.5 on 2025-02-12 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_alter_composer_options_alter_performer_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Recording",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.PositiveIntegerField()),
                ("name", models.CharField(max_length=255, unique=True)),
                ("performers", models.ManyToManyField(to="api.performer")),
                (
                    "work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.work"
                    ),
                ),
            ],
            options={
                "ordering": ["year", "work"],
            },
        ),
    ]
