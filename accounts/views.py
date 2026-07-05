import json
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (
    StudentRegistrationForm,
    StudentProfileUpdateForm,
    UserUpdateForm
)
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

    # Analytics aggregations for Phase 4 (Sprint 4.1)
    all_interactions = (
        ResourceInteraction.objects.filter(student=profile)
        .select_related("resource")
    )
    total_interactions_count = len(all_interactions)

    topic_counts = {
        "Algebra": 0,
        "Calculus": 0,
        "Programming": 0,
        "Statistics": 0,
    }
    difficulty_counts = {
        "Beginner": 0,
        "Intermediate": 0,
        "Advanced": 0,
    }

    aligned_interactions_count = 0
    rec_ids = [r["resource_id"] for r in recommendations if r.get("resource_id") is not None]

    for interaction in all_interactions:
        res = interaction.resource
        if res.topic in topic_counts:
            topic_counts[res.topic] += 1
        else:
            topic_counts[res.topic] = topic_counts.get(res.topic, 0) + 1

        if res.difficulty in difficulty_counts:
            difficulty_counts[res.difficulty] += 1
        else:
            difficulty_counts[res.difficulty] = difficulty_counts.get(res.difficulty, 0) + 1

        if res.topic == weak_topic or res.id in rec_ids:
            aligned_interactions_count += 1

    if total_interactions_count > 0:
        ai_accuracy = round((aligned_interactions_count / total_interactions_count) * 100)
    else:
        ai_accuracy = 0

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
        "topic_distribution_json": json.dumps(topic_counts),
        "difficulty_distribution_json": json.dumps(difficulty_counts),
        "ai_accuracy": ai_accuracy,
        "total_interactions_count": total_interactions_count,
    }

    return render(
        request,
        "accounts/profile.html",
        context
    )


# =========================
# USER SETTINGS
# =========================

@login_required(login_url="/accounts/login/")
def settings_view(request):

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = StudentProfileUpdateForm(
            request.POST,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()

            profile_form.save()

            messages.success(
                request,
                "Your academic profile has been successfully updated!"
            )

            return redirect(
                "settings"
            )

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = StudentProfileUpdateForm(
            instance=profile
        )

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "profile": profile,
    }

    return render(
        request,
        "accounts/settings.html",
        context
    )
