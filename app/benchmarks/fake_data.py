from app.models.health_record_model import HealthRecord


def make_fake_records(total: int) -> list[HealthRecord]:
    records: list[HealthRecord] = []

    for index in range(total):
        records.append(
            HealthRecord(
                id=index,
                record_hash=f"hash_{index}",
                type="HKQuantityTypeIdentifierHeartRate",
                source_name="Apple Watch",
                source_version="10.0",
                device="Apple Watch",
                unit="count/min",
                creation_date="2026-06-25 10:00:00-03",
                start_date="2026-06-25 10:00:00-03",
                end_date="2026-06-25 10:00:00-03",
                value=str(80 + index % 40),
                value_numeric=float(80 + index % 40),
                metadata={
                    "HKMetadataKeyHeartRateMotionContext": "1",
                },
            )
        )

    return records
