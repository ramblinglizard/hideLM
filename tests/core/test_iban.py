import pytest
from detector.core.iban import IBANDetector


@pytest.fixture
def det() -> IBANDetector:
    return IBANDetector()


def test_german_iban(det):
    matches = det.find("IBAN: DE89370400440532013000")
    assert len(matches) == 1
    assert matches[0].pii_type == "IBAN"


def test_italian_iban(det):
    matches = det.find("IT60X0542811101000000123456")
    assert len(matches) == 1


def test_gb_iban(det):
    matches = det.find("GB29NWBK60161331926819")
    assert len(matches) == 1


def test_invalid_checksum(det):
    # Wrong check digits
    assert det.find("DE00370400440532013000") == []


def test_no_match(det):
    assert det.find("Reference: AB123456") == []
