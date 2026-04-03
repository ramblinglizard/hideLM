import pytest
from detector.core.email import EmailDetector


@pytest.fixture
def det() -> EmailDetector:
    return EmailDetector()


def test_simple(det):
    matches = det.find("Contact me at john@example.com please.")
    assert len(matches) == 1
    assert matches[0].value == "john@example.com"
    assert matches[0].pii_type == "EMAIL"


def test_multiple(det):
    matches = det.find("Send to alice@corp.com and bob@corp.com")
    assert len(matches) == 2


def test_with_plus(det):
    matches = det.find("user+tag@example.com")
    assert len(matches) == 1
    assert matches[0].value == "user+tag@example.com"


def test_subdomain(det):
    matches = det.find("mail@sub.domain.co.uk is valid")
    assert len(matches) == 1


def test_no_match(det):
    assert det.find("No email here, just text.") == []


def test_position(det):
    text = "Email: hello@test.com end"
    matches = det.find(text)
    assert matches[0].start == text.index("hello@test.com")
