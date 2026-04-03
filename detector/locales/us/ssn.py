import re

from detector.base import BaseDetector, PIIMatch

# SSN format: XXX-XX-XXXX
# Excludes invalid area numbers: 000, 666, 900-999
# Excludes group 00 and serial 0000
_PATTERN = re.compile(
    r"\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b"
)


class USSSNDetector(BaseDetector):
    def find(self, text: str) -> list[PIIMatch]:
        return [
            PIIMatch(m.group(), "US_SSN", m.start(), m.end())
            for m in _PATTERN.finditer(text)
        ]
