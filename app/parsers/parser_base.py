import re
from hashlib import sha256

from decimal import Decimal
from typing import Any
from xml.etree.ElementTree import Element


class ParserBase:
    def __init__(self,):
        self.hash = sha256()
        self.empty_hash = sha256()

    def _clean_tag(self, tag: str) -> str:
        if "}" in tag:
            return tag.split("}")[-1]
        return tag

    def _safe_float(self, property: Any) -> float | None:
        try:
            decimal = Decimal(property)
            return float(decimal)
        except Exception as ex:
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
    
    def _update_file_hash(self, element: Element,):
        element_text = element.get("text", "")
        if not element_text:
            return

        element_bytes = element_text.encode("utf-8")

        if self.hash == self.empty_hash:
            self.hash = sha256(element_bytes)
            return

        self.hash.update(element_bytes)

    def _get_element_hash(self, element: Element) -> bytes:
        if element_text := element.get("text", ""):
            return sha256(element_text.encode("utf-8")).digest()
        raise Exception("Element hash was not created")

    def get_file_hash(self,) -> bytes:
        if self.hash == self.empty_hash:
            raise Exception("file hash was not created")
        return self.hash.digest()