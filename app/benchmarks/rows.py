import json
from typing import Any

from app.models.health_record_model import HealthRecord


def record_to_row(record: HealthRecord) -> tuple[Any, ...]:
    """Convert a HealthRecord dataclass to a PostgreSQL row tuple."""
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
    )
