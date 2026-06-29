from pathlib import Path

from app.benchmarks.fake_data import make_fake_records
from app.pipeline.ingestion import IngestionPipeline
from tests.repositories.fakes import FakeConnection


class FakeParser:
    def __init__(self, records: list) -> None:
        self.records = records

    def compute_file_hash(self, xml_file: Path) -> str:
        return "file_hash"

    def stream_records_elements(self, xml_file: Path):
        yield from self.records


class FakeParseRuns:
    def __init__(self, completed_exists: bool = False) -> None:
        self.completed_exists = completed_exists
        self.completed_payload: dict | None = None
        self.failed_payload: dict | None = None
        self.created_skipped = False

    def completed_run_exists(self, file_hash: str) -> bool:
        return self.completed_exists

    def create_skipped_run(self, file_hash: str, xml_file: Path) -> int:
        self.created_skipped = True
        return 99

    def create_running_run(self, file_hash: str, xml_file: Path) -> int:
        return 10

    def mark_completed(
        self,
        run_id: int,
        total_records: int,
        inserted_records: int,
        skipped_records: int,
        failed_record_count: int,
    ) -> None:
        self.completed_payload = {
            "run_id": run_id,
            "total_records": total_records,
            "inserted_records": inserted_records,
            "skipped_records": skipped_records,
            "failed_record_count": failed_record_count,
        }

    def mark_failed(self, run_id: int, error_message: str) -> None:
        self.failed_payload = {"run_id": run_id, "error_message": error_message}


class FakeHealthRecords:
    def __init__(self) -> None:
        self.chunk_sizes: list[int] = []

    def insert_many(self, records: list, parse_run_id: int) -> tuple[int, int]:
        self.chunk_sizes.append(len(records))
        return len(records), 0


def build_pipeline(records: list, completed_exists: bool = False) -> tuple[IngestionPipeline, FakeParseRuns, FakeHealthRecords]:
    pipeline = IngestionPipeline(connection=FakeConnection(), batch_size=2)  # type: ignore[arg-type]
    parse_runs = FakeParseRuns(completed_exists=completed_exists)
    health_records = FakeHealthRecords()
    pipeline.parser = FakeParser(records)  # type: ignore[assignment]
    pipeline.parse_runs = parse_runs  # type: ignore[assignment]
    pipeline.health_records = health_records  # type: ignore[assignment]
    return pipeline, parse_runs, health_records


def test_ingest_xml_marks_completed_after_batch_inserts(tmp_path: Path) -> None:
    xml_file = tmp_path / "export.xml"
    xml_file.write_text("<HealthData />", encoding="utf-8")
    records = make_fake_records(5)
    pipeline, parse_runs, health_records = build_pipeline(records)

    result = pipeline.ingest_xml(xml_file)

    assert result.status == "completed"
    assert result.parse_run_id == 10
    assert result.total_records == 5
    assert result.inserted_records == 5
    assert result.skipped_records == 0
    assert health_records.chunk_sizes == [2, 2, 1]
    assert parse_runs.completed_payload == {
        "run_id": 10,
        "total_records": 5,
        "inserted_records": 5,
        "skipped_records": 0,
        "failed_record_count": 0,
    }


def test_ingest_xml_creates_skipped_run_when_file_was_already_completed(tmp_path: Path) -> None:
    xml_file = tmp_path / "export.xml"
    xml_file.write_text("<HealthData />", encoding="utf-8")
    pipeline, parse_runs, health_records = build_pipeline([], completed_exists=True)

    result = pipeline.ingest_xml(xml_file)

    assert result.status == "skipped"
    assert result.parse_run_id == 99
    assert parse_runs.created_skipped is True
    assert health_records.chunk_sizes == []
