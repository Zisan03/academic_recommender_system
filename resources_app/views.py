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