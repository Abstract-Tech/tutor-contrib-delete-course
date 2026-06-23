"""URLs for delete_course_plugin."""

from django.urls import include, path

urlpatterns = [
    path("", include("delete_course_plugin.api.urls", namespace="api")),
]
