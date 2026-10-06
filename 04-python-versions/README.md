# 04: Python versions

## What this shows

How to install Python versions with uv, pin one for a project, and run the same code on a different version. You do not need pyenv, deadsnakes or a system package: uv downloads standalone Python builds and manages them itself.

This project is pinned to Python 3.13 and supports 3.10 and newer.

## Key config

`.python-version` holds the version uv uses for this project:

```
3.13
```

`pyproject.toml` holds the range the project supports:

```toml
[project]
requires-python = ">=3.10"
```

## Commands

### Install

```sh
uv python list                  # versions uv can download, and those already on this machine
uv python list --only-installed
uv python install 3.13          # latest 3.13.x
uv python install 3.10 3.11     # several at once
uv python install 3.12.11       # an exact patch version
uv python uninstall 3.10
```

Installing by hand is optional. If a project asks for a version that is not on the machine, `uv run` and `uv sync` download it first.

### Pin a version for the project

```sh
uv python pin 3.13              # writes .python-version
uv run main.py                  # Running on Python 3.13.x ...
```

uv refuses a pin that falls outside `requires-python`:

```
$ uv python pin 3.9
error: The requested Python version `3.9` is incompatible with the project `requires-python` value of `>=3.10`.
```

### Run on a different version once

```sh
uv run --isolated --python 3.11 main.py
```

`--python` overrides `.python-version` for one command. `--isolated` runs in a temporary environment, so the project's `.venv` stays on 3.13.

The environment variable `UV_PYTHON` does the same as `--python`. This example's CI uses it to test every supported version from one job definition:

```yaml
parallel:
  matrix:
    - UV_PYTHON: ["3.10", "3.11", "3.12", "3.13"]
```

### See what uv would use

```sh
uv python find                  # the interpreter for this project
uv python dir                   # where uv keeps the versions it downloaded
```

## Gotchas

- **`uv run --python 3.11` without `--isolated` rebuilds `.venv` on 3.11.** The next plain `uv run` rebuilds it on 3.13 again. Nothing breaks, but every switch reinstalls the dependencies.
- **uv uses a Python that is already on the machine if it matches.** A system Python 3.12 satisfies a request for 3.12, so nothing is downloaded. Pass `--managed-python` to use only versions uv installed.
- **A short version means "latest patch available".** `3.13` can resolve to different patch releases on different machines. Pin `3.13.7` when that matters.
- **Installed versions are shared, not per project.** They live in `uv python dir`. `uv python install` also puts a `python3.13` executable in `~/.local/bin`; `uv python update-shell` adds that folder to your `PATH`.
- **Downloads need internet access.** To stop uv from downloading Python, set `UV_PYTHON_DOWNLOADS=never`, or in `pyproject.toml`:

  ```toml
  [tool.uv]
  python-downloads = "never"
  ```

  uv then fails with a clear error when the version is missing. To download from an internal mirror instead, set `UV_PYTHON_INSTALL_MIRROR`.
