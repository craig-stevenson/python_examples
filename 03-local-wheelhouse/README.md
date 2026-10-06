# 03: Local wheelhouse

## What this shows

How to make uv resolve and install only from a local folder of wheels, never contacting PyPI or any other index. This is the setup for machines with no internet access.

The folder `wheels/` is committed with the two wheels this example needs, so it works straight after a clone.

## Key config

```toml
[tool.uv]
no-index = true
find-links = ["./wheels"]
```

- `no-index` tells uv to ignore PyPI.
- `find-links` lists the places to look for packages instead. The path is relative to `pyproject.toml`; an absolute path or a shared network folder also works.

Because the settings are in `pyproject.toml`, every uv command in this folder uses them. No flags are needed.

`uv.lock` records the folder, not a URL:

```toml
[[package]]
name = "six"
version = "1.17.0"
source = { registry = "wheels" }
wheels = [
    { path = "six-1.17.0-py2.py3-none-any.whl" },
]
```

## Commands

Install and run, with uv's network access switched off to prove nothing is downloaded:

```sh
uv sync --offline --no-cache
uv run --offline main.py
```

`--offline` is only there as proof. Plain `uv sync` and `uv run main.py` behave the same.

### Adding a dependency

On a machine with internet access, download the wheel and everything it depends on:

```sh
./refresh-wheels.sh some-package
```

Move the new files in `wheels/` to the offline machine (here, by committing them), then:

```sh
uv add some-package
```

uv resolves `some-package` from `wheels/` exactly as it would from PyPI. If the wheel is missing, `uv add` fails and changes nothing.

## Gotchas

- **The folder needs the whole dependency tree.** `python-dateutil` depends on `six`, so both wheels are present. `refresh-wheels.sh` uses `pip download`, which fetches dependencies for you.
- **Wheels can be platform-specific.** The two here are pure Python (`py3-none-any`) and work anywhere. A compiled package such as numpy needs the wheel for the target machine's OS, CPU and Python version. Download on a matching machine, or pass pip's `--platform` and `--python-version` flags.
- **uv does not download Python here either.** The interpreter named in `.python-version` must already be installed. Set `UV_PYTHON_DOWNLOADS=never` to get a clear error if it is not.
- **A packaged project needs its build backend in the folder.** This example has no `[build-system]` table, so uv does not build it. Add one, and the backend (for example `hatchling`) and its dependencies must be in `wheels/` too.
- **Committing wheels to git suits a demo.** For real projects, point `find-links` at a shared directory, or use an internal package index.

## Alternative spelling

The same setup written as a named index:

```toml
[[tool.uv.index]]
name = "wheelhouse"
url = "./wheels"
format = "flat"
default = true
```

`default = true` replaces PyPI. Use this form when you need to refer to the index by name, for example to pin one package to it with `[tool.uv.sources]`.
