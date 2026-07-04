from django.urls import path

from .views import (
    resource_list,
    resource_detail,
    resource_activity
)

urlpatterns = [

    path(
        "",
        resource_list,
        name="resource_list"
    ),

    path(
        "activity/",
        resource_activity,
        name="activity"
    ),

    path(
        "<int:resource_id>/",
        resource_detail,
        name="resource_detail"
    ),

]