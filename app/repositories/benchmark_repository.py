from typing import Any

from psycopg import Connection


def reset_benchmark_table(connection: Connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE benchmark_health_records RESTART IDENTITY;")

    connection.commit()


def save_benchmark_result(
    connection: Connection,
    result: dict[str, Any],
) -> None:
    sql = """
    INSERT INTO benchmark_results (
        strategy,
        input_size,
        batch_size,
        elapsed_seconds,
        rows_per_second
    )
    VALUES (%s, %s, %s, %s, %s);
    """

    with connection.cursor() as cursor:
        cursor.execute(
            sql,
            (
                result["strategy"],
                result["input_size"],
                result["batch_size"],
                result["elapsed_seconds"],
                result["rows_per_second"],
            ),
        )

    connection.commit()
