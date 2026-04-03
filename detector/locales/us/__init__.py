from detector.base import BaseDetector
from detector.locales.us.ein import USEINDetector
from detector.locales.us.ssn import USSSNDetector


def get_detectors() -> list[BaseDetector]:
    return [USSSNDetector(), USEINDetector()]
