from app.repositories.benchmark_repository import (
    reset_benchmark_table,
    save_benchmark_result,
)
from tests.repositories.fakes import FakeConnection, FakeCursor


def test_reset_benchmark_table_truncates_table_and_commits() -> None:
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    reset_benchmark_table(connection)  # type: ignore[arg-type]

    assert cursor.queries[0][0] == "TRUNCATE TABLE benchmark_health_records RESTART IDENTITY;"
    assert connection.commits == 1


def test_save_benchmark_result_inserts_metrics() -> None:
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    result = {
        "strategy": "batch_insert",
        "input_size": 1000,
        "batch_size": 100,
        "elapsed_seconds": 0.5,
        "rows_per_second": 2000.0,
    }

    save_benchmark_result(connection, result)  # type: ignore[arg-type]

    sql, params = cursor.queries[0]
    assert "INSERT INTO benchmark_results" in sql
    assert params == ("batch_insert", 1000, 100, 0.5, 2000.0)
    assert connection.commits == 1
