# 02: Adding dependencies

## What this shows

How to add, constrain, group, upgrade and remove dependencies with `uv add` and `uv remove`. Each command edits `pyproject.toml`, updates `uv.lock` and installs into `.venv` in one step.

The committed files are the end result of running the commands below in order.

## Key config

```toml
[project]
dependencies = [
    "httpx>=0.27,<1",
]

[project.optional-dependencies]
cli = [
    "rich>=15.0.0",
]

[dependency-groups]
dev = [
    "pytest>=9.1.1",
]
lint = [
    "ruff>=0.16.10",
]
```

| Table | Who gets it | Added with |
| --- | --- | --- |
| `[project] dependencies` | Everyone who installs the project | `uv add <pkg>` |
| `[project.optional-dependencies]` | Users who ask for that extra, e.g. `adding-dependencies[cli]` | `uv add --optional <extra> <pkg>` |
| `[dependency-groups]` | Developers only; never published with the package | `uv add --dev <pkg>` or `uv add --group <group> <pkg>` |

## Commands

### Add

```sh
uv add requests                 # runtime dependency; uv writes "requests>=<current version>"
uv add 'httpx>=0.27,<1'         # runtime dependency with your own constraint
uv add --dev pytest             # the "dev" group
uv add --group lint ruff        # a named group
uv add --optional cli rich      # an extra called "cli"
```

### Remove

```sh
uv remove requests              # also removes anything only requests needed
uv remove --group lint ruff     # removing from a group or extra needs the same flag
```

### Upgrade

`uv.lock` keeps versions fixed until you ask for newer ones:

```sh
uv lock --upgrade-package httpx   # newest httpx the constraint allows
uv lock --upgrade                 # everything
```

### Choose what gets installed

```sh
uv sync                         # dependencies + the "dev" group (the default)
uv sync --no-dev                # dependencies only, e.g. for production
uv sync --group lint            # also the "lint" group
uv sync --extra cli             # also the "cli" extra
uv sync --all-groups --all-extras
uv sync --locked                # fail instead of updating a stale uv.lock (use in CI)
```

### Inspect and run

```sh
uv tree                         # the resolved dependency tree
uv run main.py
uv run pytest
uv run --group lint ruff check
```

## Gotchas

- The `dev` group is installed by default; other groups and all extras are not. `uv run ruff check` fails with ``Failed to spawn: `ruff` `` unless you pass `--group lint` or have synced that group.
- `uv sync` removes packages that are not part of the requested set. Running `uv sync` after `uv sync --extra cli` uninstalls `rich`.
- `main.py` imports `rich` inside a `try` block because an extra may not be installed. Code must work without it.
- Quote constraints in the shell: `'httpx>=0.27,<1'`. Unquoted, `>` and `<` are redirections.
