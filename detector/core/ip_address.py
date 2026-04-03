import re

from detector.base import BaseDetector, PIIMatch

_IPV4 = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
    r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
)

# Full and compressed IPv6 (covers ::1, 2001:db8::, etc.)
_IPV6 = re.compile(
    r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b"
    r"|\b(?:[0-9a-fA-F]{1,4}:){1,7}:\b"
    r"|\b:(?::[0-9a-fA-F]{1,4}){1,7}\b"
)


class IPAddressDetector(BaseDetector):
    def find(self, text: str) -> list[PIIMatch]:
        results = [
            PIIMatch(m.group(), "IP_ADDRESS", m.start(), m.end())
            for m in _IPV4.finditer(text)
        ]
        results += [
            PIIMatch(m.group(), "IP_ADDRESS", m.start(), m.end())
            for m in _IPV6.finditer(text)
        ]
        return results
