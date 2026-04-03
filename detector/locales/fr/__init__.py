from detector.base import BaseDetector
from detector.locales.fr.nir import FrenchNIRDetector


def get_detectors() -> list[BaseDetector]:
    return [FrenchNIRDetector()]
