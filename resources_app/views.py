from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import (
    render,
    get_object_or_404
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