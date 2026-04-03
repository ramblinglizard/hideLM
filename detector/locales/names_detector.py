import re
from pathlib import Path

from detector.base import BaseDetector, PIIMatch

# Matches sequences of 2-4 consecutive Title-Case words
_SEQUENCE = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b")


class NamesDetector(BaseDetector):
    """
    Detects full names (2+ consecutive capitalized words) using a dictionary lookup.
    All words in the sequence must appear in the provided names file to match,
    minimizing false positives on sentence-initial capitals.
    """

    def __init__(self, *names_files: Path) -> None:
        self._names: set[str] = set()
        for path in names_files:
            if path.exists():
                with open(path, encoding="utf-8") as f:
                    for line in f:
                        name = line.strip()
                        if name and not name.startswith("#"):
                            self._names.add(name.lower())

    def find(self, text: str) -> list[PIIMatch]:
        results = []
        for m in _SEQUENCE.finditer(text):
            words = m.group().split()
            if all(w.lower() in self._names for w in words):
                results.append(PIIMatch(m.group(), "PERSON_NAME", m.start(), m.end()))
        return results
