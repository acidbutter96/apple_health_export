from collections.abc import Iterable, Iterator

from app.models.health_record_model import HealthRecord


def chunk_records(
    records: Iterable[HealthRecord],
    batch_size: int,
) -> Iterator[list[HealthRecord]]:
    """Group records into batches.

    Time complexity: O(n), because each record is visited once.
    Memory complexity: O(batch_size), because only one chunk is stored at a time.
    """
    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero")

    chunk: list[HealthRecord] = []

    for record in records:
        chunk.append(record)

        if len(chunk) >= batch_size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk
