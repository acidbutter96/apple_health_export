from app.benchmarks.fake_data import make_fake_records
from app.models.health_record_model import HealthRecord


def test_make_fake_records_returns_controlled_health_records() -> None:
    records = make_fake_records(3)

    assert len(records) == 3
    assert all(isinstance(record, HealthRecord) for record in records)
    assert [record.export_record_index for record in records] == [1, 2, 3]
    assert records[0].value == "80"
    assert records[1].value == "81"
    assert records[0].record_hash is not None
    assert len(records[0].record_hash or "") == 64


def test_make_fake_records_uses_unique_record_hashes() -> None:
    records = make_fake_records(10)

    hashes = {record.record_hash for record in records}

    assert len(hashes) == 10
