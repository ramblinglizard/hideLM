import re

from detector.base import BaseDetector, PIIMatch

# Optional IT prefix, then exactly 11 digits
_PATTERN = re.compile(r"\b(?:IT)?([0-9]{11})\b", re.IGNORECASE)


def _validate(digits: str) -> bool:
    if len(digits) != 11:
        return False
    total = 0
    for i, d in enumerate(digits[:10]):
        n = int(d)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return (10 - total % 10) % 10 == int(digits[10])


class ItalianVATDetector(BaseDetector):
    def find(self, text: str) -> list[PIIMatch]:
        results = []
        for m in _PATTERN.finditer(text):
            if _validate(m.group(1)):
                results.append(PIIMatch(m.group(), "IT_VAT", m.start(), m.end()))
        return results
