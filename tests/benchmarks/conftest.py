import pytest
from app.models.health_record_model import HealthRecord



class DummyWriter:
    name = "dummy"

    def write(self, records: list[HealthRecord]) -> int:
        return len(records)


@pytest.fixture
def dummy_writer() -> DummyWriter:
    return DummyWriter()
