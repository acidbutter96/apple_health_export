import json
import re
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from pathlib import Path
from typing import Any

from app.models.health_record_model import HealthRecord


class ParserBase:
    """Shared helper methods for parser implementations."""

    def _clean_tag(self, tag: str) -> str:
        """Remove XML namespace from an ElementTree tag.

        Example:
            "{http://www.apple.com/Health}Record" -> "Record"
        """
        if "}" in tag:
            return tag.split("}", 1)[1]
        return tag

    def _safe_float(self, value: Any) -> float | None:
        """Convert a value to float without breaking the parser.

        Apple Health values can be numeric strings, text categories, empty values,
        or missing values. Numeric values become float; everything else becomes
        None.
        """
        if value is None:
            return None

        value_as_text = str(value).strip()
        if not value_as_text:
            return None

        try:
            return float(Decimal(value_as_text))
        except (InvalidOperation, ValueError, TypeError):
            return None

    def _pascal_to_snake_case(self, value: str) -> str:
        text = value.strip()
        text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
        return text.lower()

    def compute_file_hash(self, file_path: Path, chunk_size: int = 1024 * 1024) -> str:
        """Compute a SHA-256 hash for the whole file without loading it in memory."""
        hasher = sha256()

        with file_path.open("rb") as file:
            while chunk := file.read(chunk_size):
                hasher.update(chunk)

        return hasher.hexdigest()

    def compute_record_hash(self, record: HealthRecord) -> str:
        """Compute a stable SHA-256 hash for one HealthRecord.

        Do not include database id or parser order in this hash. The goal is to
        identify the same health record across retries or across different export
        files.
        """
        stable_payload = {
            "type": record.type,
            "source_name": record.source_name,
            "source_version": record.source_version,
            "device": record.device,
            "unit": record.unit,
            "creation_date": record.creation_date,
            "start_date": record.start_date,
            "end_date": record.end_date,
            "value": record.value,
            "value_numeric": record.value_numeric,
            "metadata": record.metadata,
        }

        serialized_payload = json.dumps(
            stable_payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        return sha256(serialized_payload.encode("utf-8")).hexdigest()
