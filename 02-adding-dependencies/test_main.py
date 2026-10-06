from main import metadata_url


def test_metadata_url():
    assert str(metadata_url("uv")) == "https://pypi.org/pypi/uv/json"
