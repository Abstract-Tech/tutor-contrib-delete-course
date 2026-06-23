"""Admin registrations for delete_course_plugin."""

from django.contrib import admin

from .models import DeletedCourseRecord


@admin.register(DeletedCourseRecord)
class DeletedCourseRecordAdmin(admin.ModelAdmin):
    list_display = (
        "course_id",
        "course_title",
        "deleted_by",
        "deleted_at",
    )
    list_filter = ("deleted_at",)
    search_fields = (
        "course_id",
        "course_title",
        "deleted_by__username",
        "deleted_by__email",
    )
    ordering = ("-deleted_at",)
    readonly_fields = (
        "course_id",
        "course_title",
        "deleted_by",
        "deletion_reason",
        "deleted_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
