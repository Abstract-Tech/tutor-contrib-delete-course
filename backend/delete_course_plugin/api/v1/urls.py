"""Version 1 API URLs for delete_course_plugin."""

from django.urls import path

from .views import DeleteCourseView

app_name = "v1"

urlpatterns = [
    path("courses/<path:course_key>/delete/", DeleteCourseView.as_view(), name="delete-course"),
]
