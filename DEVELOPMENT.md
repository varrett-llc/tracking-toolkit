# Development

The extension is split into a bunch of different files. Each time you make a change, you will have to reload scripts.
To do so, click `(Blender Icon) > System > Reload Scripts`. You may bind it to a key such as `F8` for convenience.

You should install the Python dev dependencies, which includes code formatting and bpy types.

```shell
pip install -r requirements.dev.txt
```

## Code Style

Use clean and consistent code styling.
Type hints should be used where appropriate.

You must format your code using [Black](https://github.com/psf/black). You can do this by running:

```shell
black .
```

It is recommended to install the Git pre-commit hook for this:

```shell
pre-commit install
```

## Github Actions

You can use [act](https://github.com/nektos/act) to test the GitHub action workflow.

```shell
act -P windows-latest=-self-hosted -j build
```

This is usually unnecessary unless you are developing a custom CI workflow.