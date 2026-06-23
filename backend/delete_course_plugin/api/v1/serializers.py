"""Serializers for delete_course_plugin v1 APIs."""

from rest_framework import serializers


class DeleteCourseSerializer(serializers.Serializer):
    """Payload for the admin-only delete endpoint."""

    reason = serializers.CharField(required=False, allow_blank=True, max_length=1000)
