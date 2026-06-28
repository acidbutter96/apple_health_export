import psycopg
import os

from collections.abc import Iterator
from contextlib import contextmanager
from psycopg import Connection



DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://root:root@localhost:5433/apple_health",
)


@contextmanager
def get_connection() -> Iterator[Connection]:
    connection = psycopg.connect(DATABASE_URL)

    try:
        yield connection
    finally:
        connection.close()
