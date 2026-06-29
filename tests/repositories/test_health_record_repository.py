import json

from app.benchmarks.fake_data import make_fake_records
from app.repositories.health_record_repository import HealthRecordRepository
from tests.repositories.fakes import FakeConnection, FakeCursor


def test_insert_one_returns_true_when_row_was_inserted() -> None:
    cursor = FakeCursor(rowcount_values=[1])
    connection = FakeConnection(cursor)
    repository = HealthRecordRepository(connection)  # type: ignore[arg-type]
    record = make_fake_records(1)[0]

    inserted = repository.insert_one(record=record, parse_run_id=10)

    assert inserted is True
    assert "ON CONFLICT (record_hash) DO NOTHING" in cursor.queries[0][0]
    assert cursor.queries[0][1][-1] == 10
    assert connection.commits == 1


def test_insert_one_returns_false_when_record_hash_conflicts() -> None:
    cursor = FakeCursor(rowcount_values=[0])
    connection = FakeConnection(cursor)
    repository = HealthRecordRepository(connection)  # type: ignore[arg-type]
    record = make_fake_records(1)[0]

    inserted = repository.insert_one(record=record, parse_run_id=10)

    assert inserted is False
    assert connection.commits == 1


def test_insert_many_counts_inserted_and_skipped_records() -> None:
    cursor = FakeCursor(rowcount_values=[1, 0, 1])
    connection = FakeConnection(cursor)
    repository = HealthRecordRepository(connection)  # type: ignore[arg-type]
    records = make_fake_records(3)

    inserted, skipped = repository.insert_many(records=records, parse_run_id=10)

    assert inserted == 2
    assert skipped == 1
    assert len(cursor.queries) == 3
    assert connection.commits == 1


def test_insert_failed_record_serializes_raw_record_and_error_details() -> None:
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    repository = HealthRecordRepository(connection)  # type: ignore[arg-type]
    error = ValueError("bad value")

    repository.insert_failed_record(
        parse_run_id=10,
        file_hash="file_hash",
        record_index=3,
        raw_record={"value": "not-a-number"},
        error=error,
    )

    sql, params = cursor.queries[0]
    assert "INSERT INTO failed_records" in sql
    assert params[0] == 10
    assert params[1] == "file_hash"
    assert params[2] == 3
    assert json.loads(params[3]) == {"value": "not-a-number"}
    assert params[4] == "bad value"
    assert params[5] == "ValueError"
    assert connection.commits == 1
