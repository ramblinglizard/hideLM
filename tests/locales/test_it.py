import pytest
from detector.locales.it.fiscal_code import ItalianFiscalCodeDetector
from detector.locales.it.vat import ItalianVATDetector


class TestFiscalCode:
    @pytest.fixture
    def det(self) -> ItalianFiscalCodeDetector:
        return ItalianFiscalCodeDetector()

    def test_valid(self, det):
        # Real structure + valid checksum
        matches = det.find("CF: RSSMRA85M01H501Z")
        assert len(matches) == 1
        assert matches[0].pii_type == "IT_FISCAL_CODE"

    def test_invalid_checksum(self, det):
        assert det.find("RSSMRA85M01H501X") == []

    def test_no_match(self, det):
        assert det.find("Code ABC123 is not a fiscal code") == []


class TestVAT:
    @pytest.fixture
    def det(self) -> ItalianVATDetector:
        return ItalianVATDetector()

    def test_valid(self, det):
        matches = det.find("P.IVA: 12345670017")
        assert len(matches) == 1
        assert matches[0].pii_type == "IT_VAT"

    def test_with_prefix(self, det):
        matches = det.find("IT12345670017")
        assert len(matches) == 1

    def test_invalid_checksum(self, det):
        assert det.find("12345670018") == []
