from dataclasses import dataclass, field


@dataclass(slots=True,)
class HealthRecord:
    type: str | None
    source_name: str | None
    source_version: str | None
    device: str | None
    unit: str | None
    creation_date: str | None
    start_date: str | None
    end_date: str | None
    value: str | None
    value_numeric: float | None
    id: int | None = None
    record_hash: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True,)
class HealthRecordEvent:
    run_id: int
    health_record: HealthRecord
