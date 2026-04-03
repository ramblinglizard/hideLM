import pytest
from detector.core.url import URLCredentialsDetector


@pytest.fixture
def det() -> URLCredentialsDetector:
    return URLCredentialsDetector()


def test_http_credentials(det):
    matches = det.find("Connect via http://admin:secret@internal.corp/api")
    assert len(matches) == 1
    assert matches[0].pii_type == "URL_CREDENTIALS"


def test_postgres_dsn(det):
    matches = det.find("DB: postgresql://user:pass@localhost:5432/mydb")
    assert len(matches) == 1


def test_url_without_credentials(det):
    assert det.find("See https://example.com for details") == []


def test_no_match(det):
    assert det.find("user:password ratio is 1:1") == []
