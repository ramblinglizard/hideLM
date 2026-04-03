from detector.base import BaseDetector, PIIMatch
from detector.core.credit_card import CreditCardDetector
from detector.core.email import EmailDetector
from detector.core.iban import IBANDetector
from detector.core.ip_address import IPAddressDetector
from detector.core.phone import PhoneDetector
from detector.core.url import URLCredentialsDetector
from detector.locales.__loader__ import load_locale_detectors


class Detector:
    def __init__(self, settings: object) -> None:
        self._detectors: list[BaseDetector] = []

        if getattr(settings, "detect_email", True):
            self._detectors.append(EmailDetector())
        if getattr(settings, "detect_iban", True):
            self._detectors.append(IBANDetector())
        if getattr(settings, "detect_credit_card", True):
            self._detectors.append(CreditCardDetector())
        if getattr(settings, "detect_phone", True):
            self._detectors.append(PhoneDetector())
        if getattr(settings, "detect_ip", True):
            self._detectors.append(IPAddressDetector())
        if getattr(settings, "detect_url_credentials", True):
            self._detectors.append(URLCredentialsDetector())

        locales = getattr(settings, "locales", [])
        detect_names = getattr(settings, "detect_names", True)
        if locales or detect_names:
            self._detectors.extend(load_locale_detectors(locales, detect_names))

    def find_all(self, text: str) -> list[PIIMatch]:
        matches: list[PIIMatch] = []
        for det in self._detectors:
            matches.extend(det.find(text))
        matches.sort(key=lambda m: m.start)
        return _remove_overlaps(matches)


def _remove_overlaps(matches: list[PIIMatch]) -> list[PIIMatch]:
    result: list[PIIMatch] = []
    last_end = -1
    for match in matches:
        if match.start >= last_end:
            result.append(match)
            last_end = match.end
    return result
