# Tutor Contrib Delete Course

Standalone Open edX plugin for admin-only course deletion from Studio.

## Structure

- `backend/` Django app (`delete_course_plugin`) exposing API + admin model
- `frontend/` reusable Authoring MFE widget package (`@openedx/frontend-component-delete-course`)
- `tutor/` Tutor plugin that injects backend/frontend into Open edX and Authoring MFE builds

### Backend API

`POST /delete_course_plugin/v1/courses/<course_key>/delete/`

Body:

```json
{
  "reason": "optional"
}
```

### Admin model

- `DeletedCourseRecord`
- Admin label: `Deleted course records`

## Installation

Install the Tutor plugin package:

```bash
pip install tutor-contrib-delete-course
```

Enable plugin:

```bash
tutor plugins enable delete-course
```

Rebuild images so backend + authoring frontend package are injected:

```bash
tutor images build openedx mfe
```

Apply migrations in CMS:

```bash
tutor local run cms ./manage.py cms migrate delete_course_plugin
```

Restart services:

```bash
tutor local restart cms lms mfe
```

## Development

For local development from this repo root:

```bash
git clone git@github.com:Abstract-Tech/tutor-contrib-delete-course.git
cd tutor-contrib-delete-course
pip install -e .
tutor plugins enable delete-course
tutor images build openedx-dev mfe
tutor mounts add cms:/path/to/tutor-contrib-delete-course/backend:/openedx/delete-course-plugin-backend
```

## Local mounted MFE

If you are using a locally mounted `mfe/frontend-app-authoring`, local `env.config.jsx` can still be used for dev.
For staging/production, use the Tutor plugin integration in `tutor/` instead of manual env config edits.

## TODO

- Add a soft-delete/archive backup flow for deleted courses so staff/admin can restore a deleted course within a configurable retention window (for example, 30 days), after which the course is permanently deleted.
