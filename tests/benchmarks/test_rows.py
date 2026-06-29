import json

from app.benchmarks.fake_data import make_fake_records
from app.benchmarks.rows import record_to_row


def test_record_to_row_converts_health_record_to_database_tuple() -> None:
    record = make_fake_records(1)[0]

    row = record_to_row(record)

    assert row[0] == record.record_hash
    assert row[1] == record.type
    assert row[10] == record.value_numeric
    assert json.loads(row[11]) == record.metadata
