import sys


def main():
    version = ".".join(str(part) for part in sys.version_info[:3])
    print(f"Running on Python {version} at {sys.executable}")


if __name__ == "__main__":
    main()
