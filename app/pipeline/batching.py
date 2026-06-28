from collections.abc import Iterable, Iterator

from app.models.health_record_model import HealthRecord


def chunk_records(
    records: Iterable[HealthRecord],
    batch_size: int,
) -> Iterator[list[HealthRecord]]:
    chunk: list[HealthRecord] = []

    for record in records:
        chunk.append(record)

        if len(chunk) >= batch_size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk
