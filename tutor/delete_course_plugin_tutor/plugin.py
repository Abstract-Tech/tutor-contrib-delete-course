import os
from glob import glob
from pathlib import Path

try:
    from importlib import resources as importlib_resources
except Exception:
    import importlib_resources

from tutor import hooks
from tutormfe.hooks import PLUGIN_SLOTS

PLUGIN_DIR = Path(__file__).parent
PACKAGE_ROOT = PLUGIN_DIR.parent
FRONTEND_CANDIDATES = [
    PACKAGE_ROOT / "delete-course-plugin-frontend",
    PACKAGE_ROOT.parent / "frontend",
]
FRONTEND_PATH = next((p for p in FRONTEND_CANDIDATES if p.exists()), None)
BACKEND_CANDIDATES = [
    PACKAGE_ROOT / "delete-course-plugin-backend",
    PACKAGE_ROOT.parent / "backend",
]
BACKEND_PATH = next((p for p in BACKEND_CANDIDATES if p.exists()), None)

# Add the frontend and backend build contexts to the Docker build command
if FRONTEND_PATH and BACKEND_PATH:
    hooks.Filters.DOCKER_BUILD_COMMAND.add_items(
        [
            "--build-context",
            f"delete-course-plugin-frontend={str(FRONTEND_PATH)}",
            "--build-context",
            f"delete-course-plugin-backend={str(BACKEND_PATH)}",
        ]
    )


@hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_plugin(mounts, path):
    del path
    if BACKEND_PATH:
        mounts += [
            ("delete-course-plugin-backend", "/openedx/delete-course-plugin-backend")
        ]
    return mounts


for patch_path in glob(
    str(importlib_resources.files("delete_course_plugin_tutor") / "patches" / "*")
):
    with open(patch_path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(patch_path), patch_file.read())
        )

# Add the DeleteCourseButton to the authoring course outline actions slot
PLUGIN_SLOTS.add_items(
    [
        (
            "authoring",
            "org.openedx.frontend.authoring.course_outline_header_actions.v1",
            """
          {
            op: PLUGIN_OPERATIONS.Insert,
            widget: {
                id: 'delete-course-button',
                priority: 30,
                type: DIRECT_PLUGIN,
                RenderWidget: DeleteCourseButton,
            },
          }""",
        ),
    ]
)
