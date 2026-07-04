from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ML_engine.predict import generate_recommendations
from accounts.models import StudentProfile


@login_required(login_url='/accounts/login/')
def recommendation_dashboard(request):

    try:

        profile = StudentProfile.objects.get(
            user=request.user
        )

        student_id = profile.dataset_student_id

    except StudentProfile.DoesNotExist:

        student_id = 0

        profile = None

    recommendations = generate_recommendations(
        student_id
    )

    context = {
        "recommendations": recommendations,
        "student": profile,
        "username": request.user.username,
    }

    return render(
        request,
        "recommendations/dashboard.html",
        context
    )