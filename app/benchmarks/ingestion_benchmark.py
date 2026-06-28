from time import perf_counter
from typing import Any

from psycopg import Connection

from app.benchmarks.fake_data import make_fake_records
from app.benchmarks.writers import (
    BatchInsertWriter,
    CopyWriter,
    RecordWriter,
    SingleInsertWriter,
)
from app.database.connection import get_connection
from app.models.health_record_model import HealthRecord
from app.repositories.benchmark_repository import (
    reset_benchmark_table,
    save_benchmark_result,
)


def run_benchmark(
    connection: Connection,
    writer: RecordWriter,
    records: list[HealthRecord],
    batch_size: int | None = None,
) -> dict[str, Any]:
    reset_benchmark_table(connection)

    start = perf_counter()
    inserted = writer.write(records)
    elapsed = perf_counter() - start

    return {
        "strategy": writer.name,
        "input_size": inserted,
        "batch_size": batch_size,
        "elapsed_seconds": elapsed,
        "rows_per_second": inserted / elapsed,
    }


def main() -> None:
    records = make_fake_records(10_000)

    with get_connection() as connection:
        writers: list[tuple[RecordWriter, int | None]] = [
            (SingleInsertWriter(connection), None),
            (BatchInsertWriter(connection, batch_size=100), 100),
            (BatchInsertWriter(connection, batch_size=1_000), 1_000),
            (BatchInsertWriter(connection, batch_size=5_000), 5_000),
            (CopyWriter(connection), None),
        ]

        for writer, batch_size in writers:
            result = run_benchmark(
                connection=connection,
                writer=writer,
                records=records,
                batch_size=batch_size,
            )

            save_benchmark_result(connection, result)
            print(result)


if __name__ == "__main__":
    main()
