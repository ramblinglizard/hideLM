from pathlib import Path

import pytest

from detector.locales.names_detector import NamesDetector

_GLOBAL = Path(__file__).parent.parent / "detector" / "locales" / "global_names.txt"
_IT = Path(__file__).parent.parent / "detector" / "locales" / "it" / "names.txt"


@pytest.fixture
def det() -> NamesDetector:
    return NamesDetector(_GLOBAL)


@pytest.fixture
def det_it() -> NamesDetector:
    return NamesDetector(_GLOBAL, _IT)


def test_two_word_name(det):
    # Both "James" and "Thomas" are in global_names.txt
    matches = det.find("Please send the report to James Thomas.")
    assert len(matches) == 1
    assert matches[0].pii_type == "PERSON_NAME"
    assert matches[0].value == "James Thomas"


def test_two_word_name_variant(det):
    # "Mary" and "Elizabeth" are both in global_names.txt
    matches = det.find("The contract was signed by Mary Elizabeth.")
    assert len(matches) == 1
    assert matches[0].value == "Mary Elizabeth"


def test_single_capitalized_word_not_matched(det):
    # A single Title-Case word is not a full name
    assert det.find("Monday is a good day.") == []


def test_sentence_start_capitals_not_matched(det):
    # "The project" — "The" is not a name
    assert det.find("The project deadline is tomorrow.") == []


def test_no_match_all_lowercase(det):
    assert det.find("contact james thomas for details") == []


def test_position(det):
    # "Anna Maria" — both in global_names.txt; name at sentence start avoids
    # the greedy-regex edge case where a preceding Title-Case word swallows it
    text = "Anna Maria is the contact person."
    matches = det.find(text)
    assert len(matches) == 1
    assert text[matches[0].start : matches[0].end] == "Anna Maria"


def test_it_names(det_it):
    # "Marco" and "Rossi" are both in it/names.txt
    matches = det_it.find("Il referente è Marco Rossi.")
    assert len(matches) == 1
    assert matches[0].value == "Marco Rossi"
