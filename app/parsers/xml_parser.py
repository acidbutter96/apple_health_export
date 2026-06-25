import xml.etree.ElementTree as ET

from collections.abc import Iterator
from decimal import Decimal, ConversionSyntax
from pathlib import Path
from typing import Any


class XMLParser:
    def clean_tag(self, tag: str) -> str:
        if "}" in tag:
            return tag.split("}")[-1]
        return tag
    
    def safe_float(self, property: Any) -> float | None:
        try:
            decimal = Decimal(property)
            return float(decimal)
        except ConversionSyntax as ex:
            print(ex)
            return None

    def stream_records_elements(self, xml_file: Path) -> Iterator[ET.Element]:
        context = ET.iterparse(
            source=xml_file,
            events=("end",)     # could be ignored
        )
        
        for event, element in context:      #  event says if is the start or end of the tag, element it's the tag it self
            if self.clean_tag(element.tag) == "Record":
                yield element               # get the element
            element.clear()                 #   relase from memory

