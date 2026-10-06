import httpx

try:
    # Only present when the "cli" extra is installed: uv sync --extra cli
    from rich import print
except ImportError:
    pass


def metadata_url(package: str) -> httpx.URL:
    return httpx.URL("https://pypi.org").join(f"/pypi/{package}/json")


def main():
    print(f"Metadata for uv lives at {metadata_url('uv')}")


if __name__ == "__main__":
    main()
