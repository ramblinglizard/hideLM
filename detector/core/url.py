import re

from detector.base import BaseDetector, PIIMatch

# Matches URLs with embedded credentials: scheme://user:password@host
_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z0-9+\-.]*://[^\s@/]+:[^\s@/]+@\S+")


class URLCredentialsDetector(BaseDetector):
    def find(self, text: str) -> list[PIIMatch]:
        return [
            PIIMatch(m.group(), "URL_CREDENTIALS", m.start(), m.end())
            for m in _PATTERN.finditer(text)
        ]
