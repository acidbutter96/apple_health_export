from pathlib import Path

import pytest

from app.parsers import XMLProfileParser


FIXTURE_PATH = Path(__file__).parents[1] / "fixtures" / "xml" / "small_exports.xml"


def test_profile_xml_counts_all_tags_and_all_type_attributes_when_no_filter() -> None:
    profiler = XMLProfileParser()

    result = profiler.profile_xml(FIXTURE_PATH)

    assert result["tags_counter"]["Record"] == 4
    assert result["tags_counter"]["Workout"] == 1
    assert result["tags_types_counters"]["Record"]["HKQuantityTypeIdentifierHeartRate"] == 1
    assert result["tags_types_counters"]["Workout"]["<missing>"] == 1


def test_profile_xml_counts_only_requested_type_tags_when_filter_is_given() -> None:
    profiler = XMLProfileParser()

    result = profiler.profile_xml(FIXTURE_PATH, tags_to_profile={"Record"})

    assert "Record" in result["tags_types_counters"]
    assert "Workout" not in result["tags_types_counters"]


def test_profile_record_xml_requires_profile_first() -> None:
    profiler = XMLProfileParser()

    with pytest.raises(RuntimeError, match="Run profile_xml first"):
        profiler.profile_record_xml()
