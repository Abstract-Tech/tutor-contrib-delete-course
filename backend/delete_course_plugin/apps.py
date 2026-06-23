"""Django app configuration for delete_course_plugin."""

from django.apps import AppConfig
from openedx.core.djangoapps.plugins.constants import (
    PluginSettings,
    PluginURLs,
    ProjectType,
    SettingsType,
)


class DeleteCoursePluginConfig(AppConfig):
    """App configuration for course deletion plugin."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "delete_course_plugin"
    verbose_name = "Delete Course Plugin"

    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.CMS: {
                PluginURLs.NAMESPACE: "delete_course_plugin",
                PluginURLs.REGEX: r"^delete_course_plugin/",
                PluginURLs.RELATIVE_PATH: "urls",
            },
        },
        PluginSettings.CONFIG: {
            ProjectType.CMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: "settings.common",
                },
            },
        },
    }
