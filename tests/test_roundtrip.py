"""
End-to-end roundtrip tests: text with PII goes in, comes back clean.
No network calls — forwarder is mocked.
"""
import pytest
from detector.core.email import EmailDetector
from detector.core.iban import IBANDetector
from detector.core.credit_card import CreditCardDetector
from tokenizer.tokenizer import Tokenizer
from tokenizer.restorer import Restorer
from vault.vault import Vault


def _roundtrip(text: str, detectors) -> tuple[str, str]:
    vault = Vault()
    session = "rt-test"
    matches = []
    for det in detectors:
        matches.extend(det.find(text))
    matches.sort(key=lambda m: m.start)

    tokenizer = Tokenizer(session, vault)
    masked = tokenizer.mask_text(text, matches)

    restorer = Restorer(session, vault)
    restored = restorer.restore_text(masked)
    return masked, restored


def test_email_roundtrip():
    text = "Please contact john@example.com about the order."
    masked, restored = _roundtrip(text, [EmailDetector()])
    assert "john@example.com" not in masked
    assert restored == text


def test_iban_roundtrip():
    text = "Wire to DE89370400440532013000 by Friday."
    masked, restored = _roundtrip(text, [IBANDetector()])
    assert "DE89370400440532013000" not in masked
    assert restored == text


def test_credit_card_roundtrip():
    text = "Charge card 4532015112830366 for the renewal."
    masked, restored = _roundtrip(text, [CreditCardDetector()])
    assert "4532015112830366" not in masked
    assert restored == text


def test_multiple_types_roundtrip():
    text = "User alice@corp.com paid with 4532015112830366 from DE89370400440532013000."
    masked, restored = _roundtrip(
        text, [EmailDetector(), CreditCardDetector(), IBANDetector()]
    )
    assert "alice@corp.com" not in masked
    assert "4532015112830366" not in masked
    assert "DE89370400440532013000" not in masked
    assert restored == text


def test_no_pii_unchanged():
    text = "This message contains no sensitive data whatsoever."
    masked, restored = _roundtrip(text, [EmailDetector(), IBANDetector()])
    assert masked == text
    assert restored == text
