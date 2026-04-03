import re

from detector.base import BaseDetector, PIIMatch


class EmailDetector(BaseDetector):
    _pattern = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")

    def find(self, text: str) -> list[PIIMatch]:
        return [
            PIIMatch(m.group(), "EMAIL", m.start(), m.end())
            for m in self._pattern.finditer(text)
        ]
