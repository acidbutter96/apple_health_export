from pathlib import Path

import pytest

from app.models.health_record_model import HealthRecord
from app.parsers import XMLParser, XMLProfileParser


FIXTURE_PATH = Path(__file__).parents[1] / "fixtures" / "xml" / "small_exports.xml"


def test_stream_record_elements_returns_health_records_only() -> None:
    xml_parser = XMLParser()

    records = list(xml_parser.stream_records_elements(xml_file=FIXTURE_PATH))

    assert len(records) == 4
    assert all(isinstance(record, HealthRecord) for record in records)
    assert records[0].type == "HKQuantityTypeIdentifierStepCount"
    assert records[1].type == "HKQuantityTypeIdentifierHeartRate"
    assert records[1].value_numeric == 78.0
    assert records[2].value_numeric == 124.5
    assert records[0].export_record_index == 1
    assert records[3].export_record_index == 4
    assert records[0].record_hash is not None
    assert len(records[0].record_hash) == 64


def test_safe_float_returns_none_for_category_values() -> None:
    xml_parser = XMLParser()

    assert xml_parser._safe_float("92") == 92.0
    assert xml_parser._safe_float("72.5") == 72.5
    assert xml_parser._safe_float(None) is None
    assert xml_parser._safe_float("HKCategoryValueSleepAnalysisAsleepCore") is None


def test_profile_parser_counts_tags_and_record_types() -> None:
    profiler = XMLProfileParser()

    profiler.profile_xml(FIXTURE_PATH, tags_to_profile={"Record"})
    result = profiler.profile_record_xml()

    assert result["tags_counter"]["Record"] == 4
    assert result["tags_counter"]["Workout"] == 1
    assert result["record_type_counter"]["HKQuantityTypeIdentifierHeartRate"] == 1
    assert result["record_type_counter"]["HKQuantityTypeIdentifierStepCount"] == 1


def test_profile_record_xml_requires_profile_first() -> None:
    profiler = XMLProfileParser()

    with pytest.raises(RuntimeError, match="Run profile_xml first"):
        profiler.profile_record_xml()


def test_stream_record_elements_preserves_metadata_entries_until_record_is_parsed(tmp_path: Path) -> None:
    xml_file = tmp_path / "metadata_export.xml"
    xml_file.write_text(
        """
        <HealthData>
          <Record
            type="HKQuantityTypeIdentifierHeartRate"
            sourceName="Apple Watch"
            sourceVersion="11.5"
            unit="count/min"
            creationDate="2026-06-20 08:01:00 -0300"
            startDate="2026-06-20 08:00:45 -0300"
            endDate="2026-06-20 08:00:45 -0300"
            value="78">
            <MetadataEntry key="HKMetadataKeyHeartRateMotionContext" value="1" />
          </Record>
        </HealthData>
        """,
        encoding="utf-8",
    )
    xml_parser = XMLParser()

    records = list(xml_parser.stream_records_elements(xml_file=xml_file))

    assert len(records) == 1
    assert records[0].metadata == {"HKMetadataKeyHeartRateMotionContext": "1"}


def test_stream_record_events_attaches_run_id_to_each_record() -> None:
    xml_parser = XMLParser()

    events = list(xml_parser.stream_record_events(xml_file=FIXTURE_PATH, run_id=123))

    assert len(events) == 4
    assert all(event.run_id == 123 for event in events)
    assert all(isinstance(event.health_record, HealthRecord) for event in events)
