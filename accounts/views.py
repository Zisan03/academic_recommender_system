from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .forms import StudentRegistrationForm
from .models import StudentProfile
from ML_engine.predict import generate_recommendations
from resources_app.models import ResourceInteraction


# =========================
# USER REGISTRATION
# =========================

def register(request):

    if request.method == "POST":

        form = StudentRegistrationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            StudentProfile.objects.create(
                user=user
            )

            return redirect(
                "login"
            )

    else:

        form = StudentRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


# =========================
# USER LOGIN
# =========================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(
                request,
                user
            )

            return redirect(
                "recommendations"
            )

    return render(
        request,
        "accounts/login.html"
    )


# =========================
# USER LOGOUT
# =========================

def user_logout(request):

    logout(request)

    return redirect(
        "home"
    )


# =========================
# USER PROFILE
# =========================

@login_required(login_url="/accounts/login/")
def profile_view(request):

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    recent_interactions = (
        ResourceInteraction.objects.filter(
            student=profile
        )
        .select_related("resource")
        .order_by("-viewed_at")[:5]
    )

    try:
        recommendations = generate_recommendations(
            profile.dataset_student_id
        )
        recommendation_count = len(recommendations)
        weak_topic = recommendations[0]["topic"] if recommendations else "Not available"
    except Exception:
        recommendations = []
        recommendation_count = 0
        weak_topic = "Not available"

    department_display = profile.department if profile.department else "Computer Science"
    level_display = profile.level if profile.level else "400 Level"

    context = {
        "profile": profile,
        "department": department_display,
        "level": level_display,
        "recent_interactions": recent_interactions,
        "recommendation_count": recommendation_count,
        "weak_topic": weak_topic,
        "model_badge": "Hybrid Collaborative + Content-Based ML",
    }

    return render(
        request,
        "accounts/profile.html",
        context
    )
