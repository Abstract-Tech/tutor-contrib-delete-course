"""API views for delete_course_plugin."""

import logging

from django.apps import apps
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication

from ...models import DeletedCourseRecord
from ...permissions import IsSuperUserOnly
from .serializers import DeleteCourseSerializer

logger = logging.getLogger(__name__)


def _is_cms() -> bool:
    """Return True when running in Studio CMS process."""
    try:
        return apps.is_installed("cms.djangoapps.contentstore")
    except Exception:
        return False


class DeleteCourseView(APIView):
    """Delete a course from Studio and store an audit record."""

    authentication_classes = (JwtAuthentication, SessionAuthentication)
    permission_classes = [IsSuperUserOnly]

    def get(self, request, course_key):
        """
        Permission probe for frontend visibility.

        If request reaches here, user is authenticated superuser.
        """
        try:
            CourseKey.from_string(str(course_key))
        except InvalidKeyError:
            return Response(
                {"error": "Invalid course key."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "allowed": True,
                "course_id": str(course_key),
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, course_key):
        if not _is_cms():
            return Response(
                {"error": "Course deletion endpoint is only available in Studio."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = DeleteCourseSerializer(data=request.data or {})
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid request.", "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            parsed_course_key = CourseKey.from_string(str(course_key))
        except InvalidKeyError:
            return Response(
                {"error": "Invalid course key."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Import CMS-only modules lazily so LMS process imports do not break.
        from cms.djangoapps.contentstore.utils import delete_course
        from xmodule.modulestore.django import modulestore
        from xmodule.modulestore.exceptions import ItemNotFoundError

        store = modulestore()
        try:
            course = store.get_course(parsed_course_key)
        except ItemNotFoundError:
            return Response(
                {"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND
            )

        reason = serializer.validated_data.get("reason", "").strip()
        course_id = str(parsed_course_key)
        course_title = getattr(course, "display_name", "") or ""

        try:
            delete_course(parsed_course_key, request.user.id)
        except ItemNotFoundError:
            return Response(
                {"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            logger.exception("Failed to delete course %s", course_id)
            return Response(
                {"error": "Unable to delete course."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        DeletedCourseRecord.objects.create(
            course_id=course_id,
            course_title=course_title,
            deleted_by=request.user,
            deletion_reason=reason,
        )

        return Response(
            {
                "deleted": True,
                "course_id": course_id,
                "course_title": course_title,
            },
            status=status.HTTP_200_OK,
        )
