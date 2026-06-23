from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DeletedCourseRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("course_id", models.CharField(db_index=True, max_length=255)),
                ("course_title", models.CharField(blank=True, default="", max_length=255)),
                ("deletion_reason", models.TextField(blank=True, default="")),
                ("keep_instructors", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "deleted_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="deleted_course_records",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Deleted course record",
                "verbose_name_plural": "Deleted course records",
                "ordering": ["-deleted_at"],
            },
        ),
    ]
