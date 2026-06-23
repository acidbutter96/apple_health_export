import pytest
from pathlib import Path


@pytest.fixture
def tests_directory_path() -> Path:
    return Path("tests").resolve()