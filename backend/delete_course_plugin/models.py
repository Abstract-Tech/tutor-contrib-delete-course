"""Database models for delete_course_plugin."""

from django.conf import settings
from django.db import models


class DeletedCourseRecord(models.Model):
    """Audit record for one deleted course."""

    course_id = models.CharField(max_length=255, db_index=True)
    course_title = models.CharField(max_length=255, blank=True, default="")
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="deleted_course_records",
    )
    deletion_reason = models.TextField(blank=True, default="")
    deleted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Deleted course record"
        verbose_name_plural = "Deleted course records"
        ordering = ["-deleted_at"]

    def __str__(self):
        return f"{self.course_id} ({self.deleted_at.isoformat()})"
