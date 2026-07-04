from django.db import models

from accounts.models import StudentProfile
from resources_app.models import LearningResource


class InteractionHistory(models.Model):

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    resource = models.ForeignKey(
        LearningResource,
        on_delete=models.CASCADE
    )

    interaction_type = models.CharField(
        max_length=100
    )

    interaction_score = models.FloatField(
        default=1.0
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.student.user.username} "
            f"interacted with "
            f"{self.resource.title}"
        )


class RecommendationHistory(models.Model):

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    resource = models.ForeignKey(
        LearningResource,
        on_delete=models.CASCADE
    )

    recommendation_score = models.FloatField()

    recommended_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"Recommendation for "
            f"{self.student.user.username}"
        )