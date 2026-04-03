import re

from detector.base import BaseDetector, PIIMatch

# EIN format: XX-XXXXXXX with IRS-assigned valid two-digit prefixes
_PATTERN = re.compile(
    r"\b(?:0[1-6]|1[0-6]|2[0-7]|3[0-9]|4[0-8]|5[0-9]|6[0-8]|7[0-2]|7[4-7]|8[0-8]|9[0-9])-\d{7}\b"
)


class USEINDetector(BaseDetector):
    def find(self, text: str) -> list[PIIMatch]:
        return [
            PIIMatch(m.group(), "US_EIN", m.start(), m.end())
            for m in _PATTERN.finditer(text)
        ]
