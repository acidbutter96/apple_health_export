import xml.etree.ElementTree as ET

from collections.abc import Iterator
from pathlib import Path

from models.health_record_model import HealthRecord

from .parser_base import ParserBase


class XMLParser(ParserBase):
    def stream_records_elements(self, xml_file: Path) -> Iterator[ET.Element]:
        context = ET.iterparse(
            source=xml_file,
            events=("end",)     # could be ignored
        )
        
        for event, element in context:      #  event says if is the start or end of the tag, element it's the tag it self
            if self._clean_tag(element.tag) == "Record":
                yield element               # get the element
            element.clear()                 #   relase from memory

    def parse_record_element(self, element_attr: dict[str, str]) -> HealthRecord:
        ...
