from pathlib import Path

from app.models.health_record_model import HealthRecord
from app.parsers.parser_base import ParserBase


def make_record(**overrides: object) -> HealthRecord:
    data = {
        "type": "HKQuantityTypeIdentifierHeartRate",
        "source_name": "Apple Watch",
        "source_version": "11.5",
        "device": "Apple Watch",
        "unit": "count/min",
        "creation_date": "2026-06-20 08:01:00 -0300",
        "start_date": "2026-06-20 08:00:45 -0300",
        "end_date": "2026-06-20 08:00:45 -0300",
        "value": "78",
        "value_numeric": 78.0,
        "metadata": {"HKMetadataKeyHeartRateMotionContext": "1"},
    }
    data.update(overrides)
    return HealthRecord(**data)  # type: ignore[arg-type]


def test_clean_tag_removes_xml_namespace() -> None:
    parser = ParserBase()

    assert parser._clean_tag("{http://www.apple.com/Health}Record") == "Record"
    assert parser._clean_tag("Record") == "Record"


def test_safe_float_handles_numeric_and_non_numeric_values() -> None:
    parser = ParserBase()

    assert parser._safe_float("92") == 92.0
    assert parser._safe_float("72.5") == 72.5
    assert parser._safe_float("  ") is None
    assert parser._safe_float(None) is None
    assert parser._safe_float("HKCategoryValueSleepAnalysisAsleepCore") is None


def test_compute_file_hash_is_stable_and_changes_with_content(tmp_path: Path) -> None:
    parser = ParserBase()
    first = tmp_path / "first.xml"
    second = tmp_path / "second.xml"
    third = tmp_path / "third.xml"

    first.write_text("<root><Record value='1'/></root>", encoding="utf-8")
    second.write_text("<root><Record value='1'/></root>", encoding="utf-8")
    third.write_text("<root><Record value='2'/></root>", encoding="utf-8")

    assert parser.compute_file_hash(first) == parser.compute_file_hash(second)
    assert parser.compute_file_hash(first) != parser.compute_file_hash(third)


def test_compute_record_hash_is_stable_and_ignores_database_id_and_parser_index() -> None:
    parser = ParserBase()
    first = make_record(id=1, export_record_index=1)
    second = make_record(id=999, export_record_index=999)

    assert parser.compute_record_hash(first) == parser.compute_record_hash(second)


def test_compute_record_hash_changes_when_stable_content_changes() -> None:
    parser = ParserBase()
    first = make_record(value="78", value_numeric=78.0)
    second = make_record(value="79", value_numeric=79.0)

    assert parser.compute_record_hash(first) != parser.compute_record_hash(second)
