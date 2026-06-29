from app.benchmarks.fake_data import make_fake_records
from app.benchmarks.writers import BatchInsertWriter, CopyWriter, SingleInsertWriter
from tests.repositories.fakes import FakeConnection, FakeCursor


def test_single_insert_writer_executes_one_insert_per_record() -> None:
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    records = make_fake_records(3)
    writer = SingleInsertWriter(connection)  # type: ignore[arg-type]

    inserted = writer.write(records)

    assert inserted == 3
    assert len(cursor.queries) == 3
    assert all("INSERT INTO benchmark_health_records" in sql for sql, _ in cursor.queries)
    assert connection.commits == 1


def test_batch_insert_writer_executes_one_executemany_per_chunk() -> None:
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    records = make_fake_records(5)
    writer = BatchInsertWriter(connection, batch_size=2)  # type: ignore[arg-type]

    inserted = writer.write(records)

    assert inserted == 5
    assert [len(rows) for _, rows in cursor.executemany_calls] == [2, 2, 1]
    assert connection.commits == 1


def test_copy_writer_streams_every_record_to_copy() -> None:
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    records = make_fake_records(4)
    writer = CopyWriter(connection)  # type: ignore[arg-type]

    inserted = writer.write(records)

    assert inserted == 4
    assert len(cursor.copy_contexts) == 1
    assert "COPY benchmark_health_records" in cursor.copy_contexts[0].sql
    assert len(cursor.copy_contexts[0].rows) == 4
    assert connection.commits == 1
