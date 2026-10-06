# 01: Hello uv

## What this shows

The smallest useful uv project: one script, no dependencies. It introduces the four files uv works with.

| File | Purpose | Commit it? |
| --- | --- | --- |
| `pyproject.toml` | Project name, Python requirement and dependencies | Yes |
| `.python-version` | The Python version uv uses for this project | Yes |
| `uv.lock` | Exact versions of everything installed, written by uv | Yes |
| `.venv/` | The virtual environment uv creates | No |

## Key config

```toml
[project]
name = "hello-uv"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []
```

## Commands

Run the script. uv creates `.venv` and `uv.lock` first if they do not exist:

```sh
uv run main.py
```

Create or update the environment without running anything:

```sh
uv sync
```

This project was created with:

```sh
uv init --vcs none --no-workspace 01-hello-uv
```

`--vcs none` stops uv from creating a nested git repo. `--no-workspace` keeps the project standalone. In a new repo of your own, plain `uv init` is enough.

## Gotchas

- You do not activate the virtual environment. Prefix commands with `uv run` and uv uses `.venv` for you.
- Never edit `uv.lock` by hand. Change `pyproject.toml` (or use `uv add`, shown in [example 02](../02-adding-dependencies/)) and uv rewrites it.
- `requires-python` is the range the project supports. `.python-version` is the single version uv picks from that range for local work.
