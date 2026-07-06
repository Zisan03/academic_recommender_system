from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from .models import (
    LearningResource,
    ResourceInteraction
)

from accounts.models import StudentProfile


def resource_list(request):

    resources = LearningResource.objects.all()

    context = {
        "resources": resources
    }

    return render(
        request,
        "resources/resource_list.html",
        context
    )


def resource_detail(
    request,
    resource_id
):

    resource = get_object_or_404(
        LearningResource,
        id=resource_id
    )

    if request.user.is_authenticated:

        try:

            profile = StudentProfile.objects.get(
                user=request.user
            )

            ResourceInteraction.objects.create(
                student=profile,
                resource=resource
            )

        except StudentProfile.DoesNotExist:
            pass

    context = {
        "resource": resource
    }

    return render(
        request,
        "resources/resource_detail.html",
        context
    )


@login_required
def resource_activity(request):

    interactions = (
        ResourceInteraction.objects.filter(
            student__user=request.user
        )
        .select_related("resource")
        .order_by("-viewed_at")
    )

    total_views = interactions.count()

    top_topic_query = (
        interactions.values("resource__topic")
        .annotate(count=Count("id"))
        .order_by("-count")
        .first()
    )

    if top_topic_query and top_topic_query.get("resource__topic"):
        top_topic = top_topic_query["resource__topic"]
    else:
        top_topic = "None"

    if total_views > 0:
        active_status = "Active Learner 🚀"
    else:
        active_status = "No Activity Yet"

    context = {
        "interactions": interactions,
        "total_views": total_views,
        "top_topic": top_topic,
        "active_status": active_status,
    }

    return render(
        request,
        "resources/activity.html",
        context
    )


@login_required
def admin_portal(request):

    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(
            request,
            "Access denied. Administration privileges required."
        )
        return redirect("resource_list")

    resources = LearningResource.objects.all().order_by("-created_at")
    total_resources = resources.count()

    total_interactions = ResourceInteraction.objects.count()

    active_students_count = (
        ResourceInteraction.objects.values("student")
        .distinct()
        .count()
    )

    top_topic_query = (
        ResourceInteraction.objects.values("resource__topic")
        .annotate(count=Count("id"))
        .order_by("-count")
        .first()
    )

    if top_topic_query and top_topic_query.get("resource__topic"):
        top_topic = top_topic_query["resource__topic"]
    else:
        top_topic = "None"

    students = (
        StudentProfile.objects.select_related("user")
        .all()
        .order_by("user__username")
    )

    context = {
        "resources": resources,
        "total_resources": total_resources,
        "total_interactions": total_interactions,
        "active_students_count": active_students_count,
        "top_topic": top_topic,
        "students": students,
    }

    return render(
        request,
        "resources/admin_portal.html",
        context
    )


@login_required
def admin_resource_create(request):

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        topic = request.POST.get("topic", "").strip()
        difficulty = request.POST.get("difficulty", "").strip()
        resource_type = request.POST.get("resource_type", "").strip()
        description = request.POST.get("description", "").strip()
        link = request.POST.get("link", "").strip()

        if title and link:
            LearningResource.objects.create(
                title=title,
                topic=topic,
                difficulty=difficulty,
                resource_type=resource_type,
                description=description,
                link=link
            )
            messages.success(
                request,
                f"Resource '{title}' added successfully to the catalog!"
            )
        else:
            messages.error(
                request,
                "Title and link are required fields."
            )

    referer = request.META.get("HTTP_REFERER", "")
    if "manage" in referer and (request.user.is_staff or request.user.is_superuser):
        return redirect("admin_portal")
    return redirect("resource_list")


@login_required
def admin_resource_update(
    request,
    resource_id
):

    if not (request.user.is_staff or request.user.is_superuser):
        return redirect("resource_list")

    resource = get_object_or_404(
        LearningResource,
        id=resource_id
    )

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        topic = request.POST.get("topic", "").strip()
        difficulty = request.POST.get("difficulty", "").strip()
        resource_type = request.POST.get("resource_type", "").strip()
        description = request.POST.get("description", "").strip()
        link = request.POST.get("link", "").strip()

        if title and link:
            resource.title = title
            resource.topic = topic
            resource.difficulty = difficulty
            resource.resource_type = resource_type
            resource.description = description
            resource.link = link
            resource.save()

            messages.success(
                request,
                f"Resource '{title}' updated successfully!"
            )
        else:
            messages.error(
                request,
                "Title and link cannot be empty."
            )

    return redirect("admin_portal")


@login_required
def admin_resource_delete(
    request,
    resource_id
):

    resource = get_object_or_404(
        LearningResource,
        id=resource_id
    )

    if request.method == "POST":

        title = resource.title
        resource.delete()

        messages.success(
            request,
            f"Resource '{title}' deleted successfully from the catalog!"
        )

    referer = request.META.get("HTTP_REFERER", "")
    if "manage" in referer and (request.user.is_staff or request.user.is_superuser):
        return redirect("admin_portal")
    return redirect("resource_list")


@login_required
def admin_user_promote(
    request,
    user_id
):

    if not request.user.is_superuser:
        messages.error(
            request,
            "Only Chief Admins can promote or demote Delegated Admins."
        )
        return redirect("admin_portal")

    if request.method == "POST":

        target_user = get_object_or_404(
            User,
            id=user_id
        )

        if target_user == request.user:
            messages.error(
                request,
                "You cannot modify your own Chief Admin privileges."
            )
            return redirect("admin_portal")

        target_user.is_staff = not target_user.is_staff
        target_user.save()

        status_text = (
            "promoted to Delegated Admin"
            if target_user.is_staff
            else "demoted to Regular Student"
        )

        messages.success(
            request,
            f"User '{target_user.username}' successfully {status_text}!"
        )

    return redirect("admin_portal")