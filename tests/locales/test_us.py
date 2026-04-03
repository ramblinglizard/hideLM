import pytest
from detector.locales.us.ssn import USSSNDetector
from detector.locales.us.ein import USEINDetector


class TestSSN:
    @pytest.fixture
    def det(self) -> USSSNDetector:
        return USSSNDetector()

    def test_valid(self, det):
        matches = det.find("SSN: 123-45-6789")
        assert len(matches) == 1
        assert matches[0].pii_type == "US_SSN"

    def test_invalid_area_000(self, det):
        assert det.find("000-45-6789") == []

    def test_invalid_area_666(self, det):
        assert det.find("666-45-6789") == []

    def test_invalid_area_900(self, det):
        assert det.find("900-45-6789") == []

    def test_invalid_group_00(self, det):
        assert det.find("123-00-6789") == []

    def test_invalid_serial_0000(self, det):
        assert det.find("123-45-0000") == []


class TestEIN:
    @pytest.fixture
    def det(self) -> USEINDetector:
        return USEINDetector()

    def test_valid(self, det):
        matches = det.find("EIN: 12-3456789")
        assert len(matches) == 1
        assert matches[0].pii_type == "US_EIN"

    def test_no_match(self, det):
        assert det.find("99-9999999") == []
