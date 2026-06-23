"""Main API URLs for delete_course_plugin."""

from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("v1/", include("delete_course_plugin.api.v1.urls", namespace="v1")),
]
