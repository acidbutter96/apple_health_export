from pathlib import Path

from app.repositories.parse_run_repository import ParseRunRepository
from tests.repositories.fakes import FakeConnection, FakeCursor


def test_completed_run_exists_returns_database_boolean() -> None:
    cursor = FakeCursor(fetchone_values=[(True,)])
    connection = FakeConnection(cursor)
    repository = ParseRunRepository(connection)  # type: ignore[arg-type]

    exists = repository.completed_run_exists("abc")

    assert exists is True
    assert "SELECT EXISTS" in cursor.queries[0][0]
    assert cursor.queries[0][1] == ("abc",)


def test_create_running_run_returns_id_and_commits() -> None:
    cursor = FakeCursor(fetchone_values=[(42,)])
    connection = FakeConnection(cursor)
    repository = ParseRunRepository(connection)  # type: ignore[arg-type]

    run_id = repository.create_running_run("abc", Path("data/export.xml"))

    assert run_id == 42
    assert "INSERT INTO parse_runs" in cursor.queries[0][0]
    assert cursor.queries[0][1] == ("abc", "data/export.xml")
    assert connection.commits == 1


def test_mark_completed_updates_counts_and_status() -> None:
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    repository = ParseRunRepository(connection)  # type: ignore[arg-type]

    repository.mark_completed(
        run_id=7,
        total_records=10,
        inserted_records=8,
        skipped_records=2,
        failed_record_count=0,
    )

    sql, params = cursor.queries[0]
    assert "status = 'completed'" in sql
    assert params == (10, 8, 2, 0, 7)
    assert connection.commits == 1


def test_mark_failed_stores_error_message() -> None:
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    repository = ParseRunRepository(connection)  # type: ignore[arg-type]

    repository.mark_failed(run_id=7, error_message="boom")

    sql, params = cursor.queries[0]
    assert "status = 'failed'" in sql
    assert params == ("boom", 7)
    assert connection.commits == 1
