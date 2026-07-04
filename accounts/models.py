from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    age = models.IntegerField(
        null=True,
        blank=True
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    level = models.CharField(
        max_length=20,
        blank=True
    )

    dataset_student_id = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.user.username