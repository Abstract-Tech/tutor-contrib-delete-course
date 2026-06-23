from pathlib import Path
import tomllib


def test_python_package_and_tutor_plugin_names():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["name"] == "tutor-contrib-delete-course"
    assert pyproject["project"]["entry-points"]["tutor.plugin.v1"] == {
        "delete-course": "delete_course_plugin_tutor.plugin",
    }
