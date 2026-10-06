# uv examples

Small Python projects, each showing one way of configuring [uv](https://docs.astral.sh/uv/). They are numbered so you can read them in order.

| Example | What it shows | Key commands |
| --- | --- | --- |
| [01-hello-uv](01-hello-uv/) | The simplest uv project: no dependencies, one script | `uv init`, `uv run`, `uv sync` |
| [02-adding-dependencies](02-adding-dependencies/) | Adding, constraining, grouping, upgrading and removing dependencies | `uv add`, `uv remove`, `uv lock --upgrade-package` |
| [03-local-wheelhouse](03-local-wheelhouse/) | Installing from a local folder of wheels with no internet access | `no-index`, `find-links` |
| [04-python-versions](04-python-versions/) | Installing, pinning and switching between Python versions | `uv python install`, `uv python pin`, `uv run --python` |
| [05-local-python-mirror](05-local-python-mirror/) | Installing Python itself from a local folder with no internet access | `UV_PYTHON_INSTALL_MIRROR`, `uv python install --offline` |

## Running an example

Install uv ([instructions](https://docs.astral.sh/uv/getting-started/installation/)), then:

```sh
cd 01-hello-uv
uv run main.py
```

`uv run` creates the `.venv` and installs what the example needs before running it. Each example's README lists its own commands.

## How the repo is organised

Every example is a standalone uv project with its own `pyproject.toml`, `uv.lock`, `.python-version`, `README.md` and `.gitlab-ci.yml`. You can copy one folder out of the repo and it works unchanged.

There is deliberately no `pyproject.toml` at the repo root. uv looks in parent directories for a workspace, so a root project could absorb the examples and hide what each one is demonstrating.

Each `uv.lock` is committed. CI runs `uv sync --locked`, which fails if the lockfile no longer matches `pyproject.toml`.

## CI

The root [.gitlab-ci.yml](.gitlab-ci.yml) is a parent pipeline with one trigger job per example. A trigger job starts that example's own `.gitlab-ci.yml` as a child pipeline, and only when the example's folder or the shared CI config has changed.

The examples' pipelines all extend the `.uv` job in [ci/uv-base.yml](ci/uv-base.yml), which pins the uv image and sets up caching. If you copy an example into another repo, copy that job into the example's `.gitlab-ci.yml` and replace `cd "$EXAMPLE_DIR"` with whatever path applies.

To pull the uv image from an internal registry, set the `UV_IMAGE` CI/CD variable on the project.

## Adding an example

1. Create the next numbered folder: `uv init --vcs none --no-workspace NN-short-name`.
2. Give it a `README.md` with the same sections as the others, and commit its `uv.lock`.
3. Add a `.gitlab-ci.yml` that includes `ci/uv-base.yml` and extends `.uv`.
4. Add a trigger job for it in the root `.gitlab-ci.yml` and a row in the table above.
