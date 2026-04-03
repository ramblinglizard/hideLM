import re

from detector.base import BaseDetector, PIIMatch

# 11 digits, first digit 1-9 (never 0)
_PATTERN = re.compile(r"\b[1-9][0-9]{10}\b")


def _validate_iso7064(tid: str) -> bool:
    """ISO 7064 Mod 11, 10 — used by German Steueridentifikationsnummer."""
    product = 10
    for d in tid[:10]:
        total = (int(d) + product) % 10
        if total == 0:
            total = 10
        product = (2 * total) % 11
    check = 11 - product
    if check == 10:
        check = 0
    return check == int(tid[10])


class GermanTaxIDDetector(BaseDetector):
    def find(self, text: str) -> list[PIIMatch]:
        results = []
        for m in _PATTERN.finditer(text):
            if _validate_iso7064(m.group()):
                results.append(PIIMatch(m.group(), "DE_TAX_ID", m.start(), m.end()))
        return results
