import re

from detector.base import BaseDetector, PIIMatch

# ISO 13616: 2-letter country code + 2 check digits + up to 30 alphanumeric chars
_PATTERN = re.compile(r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{4,30}\b")


def _validate_mod97(iban: str) -> bool:
    iban = iban.replace(" ", "").upper()
    rearranged = iban[4:] + iban[:4]
    numeric = "".join(str(ord(c) - 55) if c.isalpha() else c for c in rearranged)
    try:
        return int(numeric) % 97 == 1
    except ValueError:
        return False


class IBANDetector(BaseDetector):
    def find(self, text: str) -> list[PIIMatch]:
        results = []
        for m in _PATTERN.finditer(text):
            if _validate_mod97(m.group()):
                results.append(PIIMatch(m.group(), "IBAN", m.start(), m.end()))
        return results
