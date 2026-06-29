from typing import Any

from app.benchmarks.fake_data import make_fake_records
from app.benchmarks.ingestion_benchmark import run_benchmark
from tests.benchmarks.conftest import DummyWriter


def test_run_benchmark_resets_table_and_returns_metrics(monkeypatch: Any, dummy_writer: DummyWriter) -> None:
    called = {"reset": False}

    def fake_reset(connection: object) -> None:
        called["reset"] = True

    monkeypatch.setattr(
        "app.benchmarks.ingestion_benchmark.reset_benchmark_table",
        fake_reset,
    )

    records = make_fake_records(5)

    result = run_benchmark(
        connection=object(),  # type: ignore[arg-type]
        writer=dummy_writer,
        records=records,
        batch_size=100,
    )

    assert called["reset"] is True
    assert result["strategy"] == "dummy"
    assert result["input_size"] == 5
    assert result["batch_size"] == 100
    assert result["elapsed_seconds"] >= 0
    assert result["rows_per_second"] >= 0
