from app.models.health_record_model import HealthRecord
from app.parsers.parser_base import ParserBase


_hash_helper = ParserBase()


def make_fake_records(total: int) -> list[HealthRecord]:
    """Create controlled fake HealthRecord objects for Chapter 6 benchmarks."""
    records: list[HealthRecord] = []

    for index in range(total):
        heart_rate = 80 + index % 40
        record = HealthRecord(
            id=None,
            export_record_index=index + 1,
            record_hash=None,
            type="HKQuantityTypeIdentifierHeartRate",
            source_name="Apple Watch",
            source_version="10.0",
            device="Apple Watch",
            unit="count/min",
            creation_date="2026-06-25 10:00:00-03",
            start_date="2026-06-25 10:00:00-03",
            end_date="2026-06-25 10:00:00-03",
            value=str(heart_rate),
            value_numeric=float(heart_rate),
            metadata={
                "HKMetadataKeyHeartRateMotionContext": "1",
            },
        )
        record.record_hash = _hash_helper.compute_record_hash(record)
        records.append(record)

    return records
