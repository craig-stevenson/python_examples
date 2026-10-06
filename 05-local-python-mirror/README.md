# 05: Local Python mirror

## What this shows

How to make uv install Python itself from a local folder instead of downloading it from GitHub. Together with [example 03](../03-local-wheelhouse/), this covers a machine with no internet access: 03 supplies the packages, this example supplies the interpreter.

[Example 04](../04-python-versions/) covers the `uv python` commands in general. This one only changes where the downloads come from.

## Key config

One environment variable points uv at the folder:

```sh
export UV_PYTHON_INSTALL_MIRROR="file://$PWD/pythons"
```

The value must be a `file://` URL with an absolute path. A relative path such as `./pythons` is rejected.

When the folder is at a fixed location on every machine, such as a shared drive, the setting can go in `pyproject.toml` instead:

```toml
[tool.uv]
python-install-mirror = "file:///mnt/shared/pythons"
```

### Folder layout

uv normally downloads from
`https://github.com/astral-sh/python-build-standalone/releases/download/<release>/<file>`.
The mirror replaces everything before `<release>`, so the folder must keep the rest:

```
pythons/
└── 20250818/
    └── cpython-3.13.7+20250818-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz
```

`pythons/` is not committed, because each build is about 30 MB. [fetch_pythons.py](fetch_pythons.py) fills it.

## Commands

### 1. On a machine with internet access: fill the folder

```sh
python3 fetch_pythons.py              # the version in .python-version
python3 fetch_pythons.py 3.11 3.12    # or specific versions
```

The script asks uv for the exact download URL (`uv python list 3.13 --only-downloads --show-urls`) and saves the file under the matching path in `pythons/`. Any Python 3.9 or newer can run it.

Copy `pythons/` to the offline machine.

### 2. On the offline machine: install from the folder

```sh
export UV_PYTHON_INSTALL_MIRROR="file://$PWD/pythons"
uv python install --offline           # installs the version in .python-version
uv run --offline main.py
```

`--offline` is only there as proof that nothing comes from the network. Without it, a plain `uv run main.py` also installs Python from the folder automatically when the version is missing.

## Gotchas

- **Fetch with the same uv version that will install.** The release date and file name are built into each uv release. A newer uv may ask for a newer build of 3.13 that is not in the folder.
- **The script fetches the build for the machine it runs on.** For a different OS or CPU, run it on a matching machine, or look up the file with `uv python list --all-platforms --show-urls`.
- **`uv run --offline` does not install Python, even from a local folder.** It reports "uv is set to offline mode". Run `uv python install --offline` first, as above.
- **The mirror is only read when Python is missing.** If the machine already has a matching Python, `uv run` and `uv sync` use that and never look in the folder.
- **This covers Python only.** Packages still come from PyPI unless you also set up a local wheel folder as in [example 03](../03-local-wheelhouse/).
