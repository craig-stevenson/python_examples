import sys


def main():
    version = ".".join(str(part) for part in sys.version_info[:3])
    print(f"Running on Python {version} installed at {sys.base_prefix}")


if __name__ == "__main__":
    main()
