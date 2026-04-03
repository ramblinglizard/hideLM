import re

from detector.base import BaseDetector, PIIMatch

# UK National Insurance Number: AA 99 99 99 A
# Invalid first-letter prefixes: D, F, I, Q, U, V
# Invalid second-letter: D, F, I, O, Q, U, V
# Invalid two-letter prefixes: BG, GB, NK, KN, NT, TN, ZZ
_PATTERN = re.compile(
    r"\b(?!BG|GB|NK|KN|NT|TN|ZZ)"
    r"[A-CEGHJ-PR-TW-Z][A-CEGHJ-NPR-TW-Z]"
    r"[0-9]{6}[A-D]\b",
    re.IGNORECASE,
)


class UKNINODetector(BaseDetector):
    def find(self, text: str) -> list[PIIMatch]:
        return [
            PIIMatch(m.group(), "GB_NINO", m.start(), m.end())
            for m in _PATTERN.finditer(text)
        ]
