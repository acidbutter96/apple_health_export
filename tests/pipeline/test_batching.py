import pytest

from app.benchmarks.fake_data import make_fake_records
from app.pipeline.batching import chunk_records


def test_chunk_records_splits_records_into_expected_batch_sizes() -> None:
    records = make_fake_records(5)

    chunks = list(chunk_records(records, batch_size=2))

    assert [len(chunk) for chunk in chunks] == [2, 2, 1]
    assert chunks[0][0] is records[0]
    assert chunks[-1][-1] is records[-1]


def test_chunk_records_accepts_generators_without_materializing_everything() -> None:
    records = (record for record in make_fake_records(3))

    chunks = list(chunk_records(records, batch_size=2))

    assert [len(chunk) for chunk in chunks] == [2, 1]


def test_chunk_records_rejects_invalid_batch_size() -> None:
    with pytest.raises(ValueError, match="batch_size must be greater than zero"):
        list(chunk_records(make_fake_records(1), batch_size=0))
