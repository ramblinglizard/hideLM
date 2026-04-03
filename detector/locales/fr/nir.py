import re

from detector.base import BaseDetector, PIIMatch

# French Numéro de Sécurité Sociale (NIR): 15 digits
# Format: [1-2][YY][MM][dept(2-3)][commune(3)][order(3)][key(2)]
_PATTERN = re.compile(r"\b[12][0-9]{2}(?:0[1-9]|1[0-2])[0-9]{8}[0-9]{2}\b")


def _validate(nir: str) -> bool:
    number = int(nir[:13])
    key = int(nir[13:])
    return (97 - number % 97) == key


class FrenchNIRDetector(BaseDetector):
    def find(self, text: str) -> list[PIIMatch]:
        results = []
        for m in _PATTERN.finditer(text):
            if _validate(m.group()):
                results.append(PIIMatch(m.group(), "FR_NIR", m.start(), m.end()))
        return results
