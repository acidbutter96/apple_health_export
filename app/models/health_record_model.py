from dataclasses import dataclass


@dataclass(slots=True,)
class HealthRecord:
    health_record_id: int
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
