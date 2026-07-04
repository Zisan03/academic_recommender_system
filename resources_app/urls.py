from django.urls import path

from .views import (
    resource_list,
    resource_detail
)

urlpatterns = [

    path(
        "",
        resource_list,
        name="resource_list"
    ),

    path(
        "<int:resource_id>/",
        resource_detail,
        name="resource_detail"
    ),

]