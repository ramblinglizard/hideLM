import pytest
from detector.core.credit_card import CreditCardDetector


@pytest.fixture
def det() -> CreditCardDetector:
    return CreditCardDetector()


def test_visa(det):
    matches = det.find("Card: 4532015112830366")
    assert len(matches) == 1
    assert matches[0].pii_type == "CREDIT_CARD"


def test_mastercard(det):
    matches = det.find("5425233430109903")
    assert len(matches) == 1


def test_amex(det):
    matches = det.find("371449635398431")
    assert len(matches) == 1


def test_invalid_luhn(det):
    # Structurally valid Visa pattern but wrong checksum
    assert det.find("4532015112830367") == []


def test_no_match(det):
    assert det.find("Call 1234567890 for info") == []
