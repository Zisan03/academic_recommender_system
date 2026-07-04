from django.contrib import admin

from .models import (
LearningResource,
ResourceInteraction
)

admin.site.register(LearningResource)
admin.site.register(ResourceInteraction)