"""Common settings for delete_course_plugin."""


def plugin_settings(settings):
    """
    Register plugin settings hook required by Open edX plugin loader.

    This plugin currently does not need custom settings, so this is a no-op.
    """
    del settings
