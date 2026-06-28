from dataclasses import dataclass
from pathlib import Path

from psycopg import Connection

from app.parsers.xml_parser import XMLParser
from app.pipeline.batching import chunk_records
from app.repositories.health_record_repository import HealthRecordRepository
from app.repositories.parse_run_repository import ParseRunRepository


@dataclass(slots=True)
class IngestionResult:
    parse_run_id: int
    file_hash: str
    status: str
    total_records: int = 0
    inserted_records: int = 0
    skipped_records: int = 0
    failed_records: int = 0


class IngestionPipeline:
    """Coordinate file hashing, parsing, batching, and idempotent insertion."""

    def __init__(self, connection: Connection, batch_size: int = 1_000) -> None:
        self.connection = connection
        self.batch_size = batch_size
        self.parser = XMLParser()
        self.parse_runs = ParseRunRepository(connection)
        self.health_records = HealthRecordRepository(connection)

    def ingest_xml(self, xml_file: Path) -> IngestionResult:
        file_hash = self.parser.compute_file_hash(xml_file)

        if self.parse_runs.completed_run_exists(file_hash):
            run_id = self.parse_runs.create_skipped_run(file_hash, xml_file)
            return IngestionResult(
                parse_run_id=run_id,
                file_hash=file_hash,
                status="skipped",
            )

        run_id = self.parse_runs.create_running_run(file_hash, xml_file)

        total_records = 0
        inserted_records = 0
        skipped_records = 0
        failed_records = 0

        try:
            records = self.parser.stream_records_elements(xml_file)

            for chunk in chunk_records(records, self.batch_size):
                total_records += len(chunk)
                inserted, skipped = self.health_records.insert_many(
                    records=chunk,
                    parse_run_id=run_id,
                )
                inserted_records += inserted
                skipped_records += skipped

            self.parse_runs.mark_completed(
                run_id=run_id,
                total_records=total_records,
                inserted_records=inserted_records,
                skipped_records=skipped_records,
                failed_record_count=failed_records,
            )

            return IngestionResult(
                parse_run_id=run_id,
                file_hash=file_hash,
                status="completed",
                total_records=total_records,
                inserted_records=inserted_records,
                skipped_records=skipped_records,
                failed_records=failed_records,
            )
        except Exception as error:
            self.parse_runs.mark_failed(run_id=run_id, error_message=str(error))
            raise
