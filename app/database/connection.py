import psycopg
import os
from collections.abc import Iterator
from contextlib import contextmanager

from psycopg import Connection


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://root:root@localhost:5444/apple_health_export_db",
)


@contextmanager
def get_connection() -> Iterator[Connection]:
    """Open and close a PostgreSQL connection."""
    connection = psycopg.connect(DATABASE_URL)

    try:
        yield connection
    finally:
        connection.close()
