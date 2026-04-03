import importlib
from pathlib import Path

from detector.base import BaseDetector
from detector.locales.names_detector import NamesDetector

_LOCALES_DIR = Path(__file__).parent
_GLOBAL_NAMES = _LOCALES_DIR / "global_names.txt"


def load_locale_detectors(locales: list[str], detect_names: bool) -> list[BaseDetector]:
    detectors: list[BaseDetector] = []
    names_files: list[Path] = []

    for locale in locales:
        try:
            module = importlib.import_module(f"detector.locales.{locale}")
            detectors.extend(module.get_detectors())
        except ModuleNotFoundError:
            print(f"[hideLM] locale '{locale}' not found, skipping")
            continue

        locale_names = _LOCALES_DIR / locale / "names.txt"
        if locale_names.exists():
            names_files.append(locale_names)

    if detect_names:
        # Always include the global fallback dictionary
        if _GLOBAL_NAMES.exists():
            names_files.append(_GLOBAL_NAMES)
        if names_files:
            detectors.append(NamesDetector(*names_files))

    return detectors
