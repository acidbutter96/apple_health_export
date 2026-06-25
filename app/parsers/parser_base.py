import re

from decimal import ConversionSyntax, Decimal
from typing import Any


class ParserBase:
    def _clean_tag(self, tag: str) -> str:
        if "}" in tag:
            return tag.split("}")[-1]
        return tag

    def _safe_float(self, property: Any) -> float | None:
        try:
            decimal = Decimal(property)
            return float(decimal)
        except ConversionSyntax as ex:
            print(ex)
            return None

    def _pascal_to_snake_case(self, value: str) -> str:
        text = value.strip()

        text = re.sub(
            r"([a-z0-9])([A-Z])",  # () -> capture group lowercase/number [a-z0-9] before a upper caseletter ([A-Z])
            r"\1_\2",       # \1 group 1 _ \2 group2
            text,
        )

        return text.lower()