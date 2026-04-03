from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PIIMatch:
    value: str      # original text found
    pii_type: str   # e.g. "EMAIL", "IBAN", "IT_FISCAL_CODE"
    start: int      # start index in source text
    end: int        # end index in source text


class BaseDetector(ABC):
    @abstractmethod
    def find(self, text: str) -> list[PIIMatch]:
        ...
