from detector.base import BaseDetector
from detector.locales.de.steuer_id import GermanTaxIDDetector


def get_detectors() -> list[BaseDetector]:
    return [GermanTaxIDDetector()]
