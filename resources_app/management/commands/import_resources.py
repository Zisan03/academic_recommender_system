from django.core.management.base import BaseCommand

import pandas as pd

from resources_app.models import LearningResource
from ML_engine.config import RESOURCES_DATASET


class Command(BaseCommand):

    help = "Import learning resources from CSV"

    def handle(self, *args, **kwargs):

        df = pd.read_csv(RESOURCES_DATASET)

        count = 0

        for _, row in df.iterrows():

            resource, created = (
                LearningResource.objects.get_or_create(
                    title=row["title"],
                    defaults={
                        "topic": row["topic"],
                        "difficulty": row["difficulty"],
                        "resource_type": row["type"],
                        "description": row.get(
                            "description",
                            "Learning resource"
                        ),
                        "link": "https://example.com"
                    }
                )
            )

            if created:
                count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} resources imported successfully."
            )
        )