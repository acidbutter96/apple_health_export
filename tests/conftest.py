"""Shared pytest helpers.

The production project depends on psycopg, but most unit tests use fake
connections and do not need a real PostgreSQL driver. This fallback lets the
unit test suite run in minimal environments where psycopg is not installed.
When psycopg is installed, this file does nothing.
"""

from __future__ import annotations

import sys
import types

try:  # pragma: no cover - real project environments should use psycopg.
    import psycopg as _psycopg  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover - test-only fallback.
    psycopg_stub = types.ModuleType("psycopg")

    class Connection:  # type: ignore[no-redef]
        pass

    def connect(*_args: object, **_kwargs: object) -> Connection:
        raise RuntimeError(
            "psycopg is not installed. Install it with: poetry add 'psycopg[binary]'"
        )

    psycopg_stub.Connection = Connection
    psycopg_stub.connect = connect
    sys.modules["psycopg"] = psycopg_stub
