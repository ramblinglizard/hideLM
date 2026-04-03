import phonenumbers

from detector.base import BaseDetector, PIIMatch


class PhoneDetector(BaseDetector):
    """
    Detects phone numbers in any country using Google's libphonenumber.
    Handles E.164, national, and international formats without locale config.
    """

    def find(self, text: str) -> list[PIIMatch]:
        results = []
        for match in phonenumbers.PhoneNumberMatcher(text, None):
            results.append(
                PIIMatch(match.raw_string, "PHONE", match.start, match.end)
            )
        return results
