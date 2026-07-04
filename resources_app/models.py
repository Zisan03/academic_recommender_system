from django.db import models


class LearningResource(models.Model):

    TOPIC_CHOICES = [
        ("Algebra", "Algebra"),
        ("Calculus", "Calculus"),
        ("Programming", "Programming"),
        ("Statistics", "Statistics"),
    ]

    DIFFICULTY_CHOICES = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    RESOURCE_TYPES = [
        ("Video", "Video"),
        ("PDF", "PDF"),
        ("Practice", "Practice"),
    ]

    title = models.CharField(
        max_length=255
    )

    topic = models.CharField(
        max_length=100,
        choices=TOPIC_CHOICES
    )

    difficulty = models.CharField(
        max_length=100,
        choices=DIFFICULTY_CHOICES
    )

    resource_type = models.CharField(
        max_length=100,
        choices=RESOURCE_TYPES
    )

    description = models.TextField()

    link = models.URLField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class ResourceInteraction(models.Model):

    student = models.ForeignKey(
        "accounts.StudentProfile",
        on_delete=models.CASCADE
    )

    resource = models.ForeignKey(
        LearningResource,
        on_delete=models.CASCADE
    )

    viewed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.student.user.username} viewed "
            f"{self.resource.title}"
        )
