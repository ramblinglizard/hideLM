import pytest
from detector.core.ip_address import IPAddressDetector


@pytest.fixture
def det() -> IPAddressDetector:
    return IPAddressDetector()


def test_ipv4(det):
    matches = det.find("Server at 203.0.113.42 responded.")
    assert len(matches) == 1
    assert matches[0].value == "203.0.113.42"
    assert matches[0].pii_type == "IP_ADDRESS"


def test_ipv4_private_still_detected(det):
    # Private IPs are still detected; admin can disable the whole detector
    matches = det.find("Gateway: 192.168.1.1")
    assert len(matches) == 1


def test_ipv4_invalid_octet(det):
    assert det.find("999.999.999.999") == []


def test_ipv6_full(det):
    matches = det.find("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    assert len(matches) == 1


def test_no_match(det):
    assert det.find("Version 1.2.3 released") == []
