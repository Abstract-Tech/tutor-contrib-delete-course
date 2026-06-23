#!/usr/bin/env python
"""Package metadata for delete_course_plugin."""

from setuptools import find_packages, setup


setup(
    name="delete-course-plugin",
    version="1.0.0",
    description="Admin-only course deletion plugin for Open edX Studio",
    packages=find_packages(include=["delete_course_plugin", "delete_course_plugin.*"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=[],
    entry_points={
        "lms.djangoapp": [
            "delete_course_plugin = delete_course_plugin.apps:DeleteCoursePluginConfig",
        ],
        "cms.djangoapp": [
            "delete_course_plugin = delete_course_plugin.apps:DeleteCoursePluginConfig",
        ],
    },
)
