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