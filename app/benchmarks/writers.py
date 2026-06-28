from typing import Protocol

from psycopg import Connection

from app.benchmarks.rows import record_to_row
from app.models.health_record_model import HealthRecord
from app.pipeline.batching import chunk_records


INSERT_SQL = """
INSERT INTO benchmark_health_records (
    record_hash,
    type,
    source_name,
    source_version,
    device,
    unit,
    creation_date,
    start_date,
    end_date,
    value,
    value_numeric,
    metadata
)
VALUES (
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s::jsonb
);
"""


class RecordWriter(Protocol):
    name: str

    def write(self, records: list[HealthRecord]) -> int: ...


class SingleInsertWriter:
    name = "single_insert"

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def write(self, records: list[HealthRecord]) -> int:
        with self.connection.cursor() as cursor:
            for record in records:
                cursor.execute(INSERT_SQL, record_to_row(record))

        self.connection.commit()
        return len(records)


class BatchInsertWriter:
    name = "batch_insert"

    def __init__(
        self,
        connection: Connection,
        batch_size: int,
    ) -> None:
        self.connection = connection
        self.batch_size = batch_size

    def write(self, records: list[HealthRecord]) -> int:
        inserted = 0

        with self.connection.cursor() as cursor:
            for chunk in chunk_records(records, self.batch_size):
                rows = [record_to_row(record) for record in chunk]
                cursor.executemany(INSERT_SQL, rows)
                inserted += len(chunk)

        self.connection.commit()
        return inserted


class CopyWriter:
    name = "copy"

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def write(self, records: list[HealthRecord]) -> int:
        copy_sql = """
        COPY benchmark_health_records (
            record_hash,
            type,
            source_name,
            source_version,
            device,
            unit,
            creation_date,
            start_date,
            end_date,
            value,
            value_numeric,
            metadata
        )
        FROM STDIN
        """

        with self.connection.cursor() as cursor:
            with cursor.copy(copy_sql) as copy:
                for record in records:
                    copy.write_row(record_to_row(record))

        self.connection.commit()
        return len(records)
