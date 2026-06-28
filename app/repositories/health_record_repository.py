import json
from typing import Any

from psycopg import Connection

from app.models.health_record_model import HealthRecord


INSERT_HEALTH_RECORD_SQL = """
INSERT INTO health_records (
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
    metadata,
    parse_run_id
)
VALUES (
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s::jsonb, %s
)
ON CONFLICT (record_hash) DO NOTHING;
"""


class HealthRecordRepository:
    """SQL operations for parsed health records and failed rows."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def insert_one(self, record: HealthRecord, parse_run_id: int) -> bool:
        with self.connection.cursor() as cursor:
            cursor.execute(
                INSERT_HEALTH_RECORD_SQL,
                self._record_to_params(record, parse_run_id),
            )
            inserted = cursor.rowcount == 1

        self.connection.commit()
        return inserted

    def insert_many(self, records: list[HealthRecord], parse_run_id: int) -> tuple[int, int]:
        inserted_count = 0
        skipped_count = 0

        with self.connection.cursor() as cursor:
            for record in records:
                cursor.execute(
                    INSERT_HEALTH_RECORD_SQL,
                    self._record_to_params(record, parse_run_id),
                )
                if cursor.rowcount == 1:
                    inserted_count += 1
                else:
                    skipped_count += 1

        self.connection.commit()
        return inserted_count, skipped_count

    def insert_failed_record(
        self,
        parse_run_id: int,
        file_hash: str,
        record_index: int | None,
        raw_record: dict[str, Any] | None,
        error: Exception,
    ) -> None:
        sql = """
        INSERT INTO failed_records (
            parse_run_id,
            file_hash,
            record_index,
            raw_record,
            error_message,
            error_type
        )
        VALUES (%s, %s, %s, %s::jsonb, %s, %s);
        """

        raw_record_json = json.dumps(raw_record or {}, sort_keys=True)

        with self.connection.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    parse_run_id,
                    file_hash,
                    record_index,
                    raw_record_json,
                    str(error),
                    type(error).__name__,
                ),
            )

        self.connection.commit()

    def _record_to_params(self, record: HealthRecord, parse_run_id: int) -> tuple[Any, ...]:
        return (
            record.record_hash,
            record.type,
            record.source_name,
            record.source_version,
            record.device,
            record.unit,
            record.creation_date,
            record.start_date,
            record.end_date,
            record.value,
            record.value_numeric,
            json.dumps(record.metadata, sort_keys=True),
            parse_run_id,
        )
