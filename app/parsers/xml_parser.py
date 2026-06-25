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

    def metadata_parser(self, element: ET.Element) -> dict[str, str]:
        metadata = {}
        for child in element:
            child_tag = self._clean_tag(child.tag)
            if child_tag != "MetadataEntry":
                continue
            key, value = child.attrib.get("key"), child.attrib.get("value")

            if key and value:
                metadata[key] = value
        return metadata

    def parse_record_element(
        self,
        element: ET.Element,
        run_id: int,
    ) -> HealthRecord:
        attrs = element.attrib
        value = attrs.get("value")

        return HealthRecord(
            health_record_id=run_id,
            type=attrs.get("type"),
            creation_date=attrs.get("creationDate"),
            device=attrs.get("device"),
            source_name=attrs.get("sourceName"),
            source_version=attrs.get("sourceVersion"),
            unit=attrs.get("unit"),
            start_date=attrs.get("startDate"),
            end_date=attrs.get("endDate"),
            value=value,
            value_numeric=self._safe_float(value),
            metadata=self.metadata_parser(element),
        )
