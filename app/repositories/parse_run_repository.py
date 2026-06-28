from pathlib import Path

from psycopg import Connection


class ParseRunRepository:
    """SQL operations for file-level ingestion attempts."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def completed_run_exists(self, file_hash: str) -> bool:
        sql = """
        SELECT EXISTS (
            SELECT 1
            FROM parse_runs
            WHERE file_hash = %s
              AND status = 'completed'
        );
        """

        with self.connection.cursor() as cursor:
            cursor.execute(sql, (file_hash,))
            return bool(cursor.fetchone()[0])

    def create_running_run(self, file_hash: str, file_path: Path) -> int:
        sql = """
        INSERT INTO parse_runs (file_hash, file_path, status)
        VALUES (%s, %s, 'running')
        RETURNING id;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(sql, (file_hash, str(file_path)))
            run_id = cursor.fetchone()[0]

        self.connection.commit()
        return int(run_id)

    def create_skipped_run(self, file_hash: str, file_path: Path) -> int:
        sql = """
        INSERT INTO parse_runs (file_hash, file_path, status, finished_at)
        VALUES (%s, %s, 'skipped', now())
        RETURNING id;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(sql, (file_hash, str(file_path)))
            run_id = cursor.fetchone()[0]

        self.connection.commit()
        return int(run_id)

    def mark_completed(
        self,
        run_id: int,
        total_records: int,
        inserted_records: int,
        skipped_records: int,
        failed_record_count: int,
    ) -> None:
        sql = """
        UPDATE parse_runs
        SET status = 'completed',
            finished_at = now(),
            total_records = %s,
            inserted_records = %s,
            skipped_records = %s,
            failed_record_count = %s
        WHERE id = %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    total_records,
                    inserted_records,
                    skipped_records,
                    failed_record_count,
                    run_id,
                ),
            )

        self.connection.commit()

    def mark_failed(self, run_id: int, error_message: str) -> None:
        sql = """
        UPDATE parse_runs
        SET status = 'failed',
            finished_at = now(),
            error_message = %s
        WHERE id = %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(sql, (error_message, run_id))

        self.connection.commit()
