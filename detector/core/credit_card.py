import re

from detector.base import BaseDetector, PIIMatch

# Covers Visa (13/16), Mastercard (16), Amex (15), Discover (16)
_PATTERN = re.compile(
    r"\b(?:"
    r"4[0-9]{12}(?:[0-9]{3})?"         # Visa
    r"|5[1-5][0-9]{14}"                 # Mastercard
    r"|3[47][0-9]{13}"                  # Amex
    r"|6(?:011|5[0-9]{2})[0-9]{12}"    # Discover
    r")\b"
)


def _luhn(number: str) -> bool:
    digits = [int(d) for d in number]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for d in even_digits:
        total += sum(divmod(d * 2, 10))
    return total % 10 == 0


class CreditCardDetector(BaseDetector):
    def find(self, text: str) -> list[PIIMatch]:
        results = []
        for m in _PATTERN.finditer(text):
            digits = re.sub(r"\D", "", m.group())
            if _luhn(digits):
                results.append(PIIMatch(m.group(), "CREDIT_CARD", m.start(), m.end()))
        return results
