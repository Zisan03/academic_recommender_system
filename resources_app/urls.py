from django.urls import path

from .views import (
    resource_list,
    resource_detail,
    resource_activity,
    admin_portal,
    admin_resource_create,
    admin_resource_update,
    admin_resource_delete,
    admin_user_promote,
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
        "manage/",
        admin_portal,
        name="admin_portal"
    ),

    path(
        "manage/add/",
        admin_resource_create,
        name="admin_resource_create"
    ),

    path(
        "manage/edit/<int:resource_id>/",
        admin_resource_update,
        name="admin_resource_update"
    ),

    path(
        "manage/delete/<int:resource_id>/",
        admin_resource_delete,
        name="admin_resource_delete"
    ),

    path(
        "manage/promote/<int:user_id>/",
        admin_user_promote,
        name="admin_user_promote"
    ),

    path(
        "<int:resource_id>/",
        resource_detail,
        name="resource_detail"
    ),

]