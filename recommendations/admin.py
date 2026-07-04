from django.contrib import admin

from .models import (
    InteractionHistory,
    RecommendationHistory
)


admin.site.register(InteractionHistory)

admin.site.register(RecommendationHistory)