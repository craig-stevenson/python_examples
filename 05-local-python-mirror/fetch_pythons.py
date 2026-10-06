"""Download Python builds into ./pythons. Run on a machine WITH internet access.

Usage: python3 fetch_pythons.py [VERSION ...]

With no arguments it fetches the version in .python-version.
Needs only uv and the standard library (Python 3.9+).
"""

import json
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
MIRROR = HERE / "pythons"
# uv swaps this prefix for the mirror and keeps the rest of the URL,
# so the folder must repeat the upstream layout: <release>/<file name>.
UPSTREAM = "https://github.com/astral-sh/python-build-standalone/releases/download/"


def download_url(version: str) -> str:
    """Ask uv which build it would download for this version on this machine."""
    listing = subprocess.run(
        ["uv", "python", "list", version, "--only-downloads", "--show-urls", "--output-format", "json"],
        check=True,
        capture_output=True,
        text=True,
    )
    # The listing can also include PyPy, GraalPy and free-threaded builds.
    builds = [
        build
        for build in json.loads(listing.stdout)
        if build["implementation"] == "cpython" and build["variant"] == "default"
    ]
    if not builds:
        sys.exit(f"uv has no download for Python {version} on this platform")
    return builds[0]["url"]


def main():
    versions = sys.argv[1:] or [(HERE / ".python-version").read_text().strip()]
    for version in versions:
        url = download_url(version)
        if not url.startswith(UPSTREAM):
            sys.exit(f"Unexpected download location for Python {version}: {url}")
        # The URL encodes "+" as "%2B"; the file on disk needs the real "+".
        target = MIRROR / urllib.parse.unquote(url.removeprefix(UPSTREAM))
        if target.exists():
            print(f"Already have {target.relative_to(HERE)}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading {url}")
        urllib.request.urlretrieve(url, target)
        print(f"Saved {target.relative_to(HERE)}")


if __name__ == "__main__":
    main()
