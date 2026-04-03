from detector.base import BaseDetector
from detector.locales.gb.nino import UKNINODetector


def get_detectors() -> list[BaseDetector]:
    return [UKNINODetector()]
