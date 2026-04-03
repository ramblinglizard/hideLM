import re

from detector.base import BaseDetector, PIIMatch

_PATTERN = re.compile(
    r"\b[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]\b",
    re.IGNORECASE,
)

# Official odd-position lookup table (Agenzia delle Entrate)
_ODD: dict[str, int] = {
    "0": 1,  "1": 0,  "2": 5,  "3": 7,  "4": 9,  "5": 13, "6": 15, "7": 17,
    "8": 19, "9": 21, "A": 1,  "B": 0,  "C": 5,  "D": 7,  "E": 9,  "F": 13,
    "G": 15, "H": 17, "I": 19, "J": 21, "K": 2,  "L": 4,  "M": 18, "N": 20,
    "O": 11, "P": 3,  "Q": 6,  "R": 8,  "S": 12, "T": 14, "U": 16, "V": 10,
    "W": 22, "X": 25, "Y": 24, "Z": 23,
}


def _validate(cf: str) -> bool:
    cf = cf.upper()
    total = 0
    for i, c in enumerate(cf[:15]):
        # positions are 1-indexed: odd positions use _ODD table
        if (i + 1) % 2 == 1:
            total += _ODD[c]
        else:
            total += int(c) if c.isdigit() else (ord(c) - ord("A"))
    return cf[15] == chr(total % 26 + ord("A"))


class ItalianFiscalCodeDetector(BaseDetector):
    def find(self, text: str) -> list[PIIMatch]:
        results = []
        for m in _PATTERN.finditer(text):
            if _validate(m.group()):
                results.append(PIIMatch(m.group(), "IT_FISCAL_CODE", m.start(), m.end()))
        return results
