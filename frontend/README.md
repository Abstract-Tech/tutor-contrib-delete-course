# Delete Course Frontend Package

Reusable Authoring MFE widget package:

This package is intended to be injected into Authoring MFE during image build,
then registered through plugin slots runtime config.

## Install and build

```bash
cd frontend
npm install
npm run build
```

## Dev sync for mounted Authoring MFE

If you are running `tutor dev` with mounted Authoring app (`mfe/frontend-app-authoring`),
sync the built `dist` into the mounted plugin directory:

```bash
rsync -a --delete dist/ /path/to/frontend-app-authoring/plugins/frontend-component-delete-course/dist/
tutor dev restart authoring
```
