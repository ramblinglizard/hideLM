from detector.base import BaseDetector
from detector.locales.it.fiscal_code import ItalianFiscalCodeDetector
from detector.locales.it.vat import ItalianVATDetector


def get_detectors() -> list[BaseDetector]:
    return [ItalianFiscalCodeDetector(), ItalianVATDetector()]
