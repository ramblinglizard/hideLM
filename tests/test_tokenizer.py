import pytest
from detector.base import PIIMatch
from tokenizer.tokenizer import Tokenizer
from tokenizer.restorer import Restorer
from vault.vault import Vault


@pytest.fixture
def vault() -> Vault:
    return Vault()  # in-memory


def test_mask_single(vault):
    t = Tokenizer("s1", vault)
    text = "Email me at john@example.com please"
    matches = [PIIMatch("john@example.com", "EMAIL", 12, 28)]
    result = t.mask_text(text, matches)
    assert "john@example.com" not in result
    assert "[EMAIL_1]" in result


def test_same_value_same_token(vault):
    t = Tokenizer("s2", vault)
    m1 = [PIIMatch("alice@corp.com", "EMAIL", 0, 14)]
    m2 = [PIIMatch("alice@corp.com", "EMAIL", 4, 18)]
    r1 = t.mask_text("alice@corp.com here", m1)
    r2 = t.mask_text("cc: alice@corp.com", m2)
    token1 = r1.split()[0]
    token2 = r2.split()[1]
    assert token1 == token2


def test_different_values_different_tokens(vault):
    t = Tokenizer("s3", vault)
    text = "From alice@a.com to bob@b.com"
    matches = [
        PIIMatch("alice@a.com", "EMAIL", 5, 16),
        PIIMatch("bob@b.com", "EMAIL", 20, 29),
    ]
    result = t.mask_text(text, matches)
    assert "[EMAIL_1]" in result
    assert "[EMAIL_2]" in result


def test_restore(vault):
    t = Tokenizer("s4", vault)
    r = Restorer("s4", vault)
    original = "Contact john@example.com ASAP"
    matches = [PIIMatch("john@example.com", "EMAIL", 8, 24)]
    masked = t.mask_text(original, matches)
    restored = r.restore_text(masked)
    assert restored == original


def test_unknown_token_left_intact(vault):
    r = Restorer("s5", vault)
    text = "Hello [EMAIL_1] world"
    # No mapping stored — token should be left as-is
    assert r.restore_text(text) == text
