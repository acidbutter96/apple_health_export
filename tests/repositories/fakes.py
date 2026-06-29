from collections.abc import Iterable
from typing import Any


class FakeCursor:
    def __init__(
        self,
        fetchone_values: list[tuple[Any, ...]] | None = None,
        rowcount_values: list[int] | None = None,
    ) -> None:
        self.queries: list[tuple[str, tuple[Any, ...] | None]] = []
        self.fetchone_values = fetchone_values or []
        self.rowcount_values = rowcount_values or []
        self.rowcount = 0
        self.executemany_calls: list[tuple[str, list[tuple[Any, ...]]]] = []
        self.copy_contexts: list[FakeCopy] = []

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def execute(self, sql: str, params: tuple[Any, ...] | None = None) -> None:
        self.queries.append((sql, params))
        if self.rowcount_values:
            self.rowcount = self.rowcount_values.pop(0)

    def executemany(self, sql: str, rows: Iterable[tuple[Any, ...]]) -> None:
        rows_as_list = list(rows)
        self.executemany_calls.append((sql, rows_as_list))
        self.rowcount = len(rows_as_list)

    def fetchone(self) -> tuple[Any, ...]:
        return self.fetchone_values.pop(0)

    def copy(self, sql: str) -> "FakeCopy":
        copy = FakeCopy(sql)
        self.copy_contexts.append(copy)
        return copy


class FakeCopy:
    def __init__(self, sql: str) -> None:
        self.sql = sql
        self.rows: list[tuple[Any, ...]] = []

    def __enter__(self) -> "FakeCopy":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def write_row(self, row: tuple[Any, ...]) -> None:
        self.rows.append(row)


class FakeConnection:
    def __init__(self, cursor: FakeCursor | None = None) -> None:
        self.cursor_instance = cursor or FakeCursor()
        self.commits = 0
        self.closed = False

    def cursor(self) -> FakeCursor:
        return self.cursor_instance

    def commit(self) -> None:
        self.commits += 1

    def close(self) -> None:
        self.closed = True
