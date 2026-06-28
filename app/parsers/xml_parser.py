import xml.etree.ElementTree as ET

from collections.abc import Iterator
from pathlib import Path

from models.health_record_model import HealthRecord

from parsers.parser_base import ParserBase


class XMLParser(ParserBase):
    def stream_records_elements(self, xml_file: Path) -> Iterator[HealthRecord]:
        context = ET.iterparse(
            source=xml_file,
            events=("end",)     # could be ignored
        )


        for event, element in context:      #  event says if is the start or end of the tag, element it's the tag it self
            try:
                self._update_file_hash(element)
            except Exception:
                print("file hash was not created\n deal with problem")
            
            if self._clean_tag(element.tag) == "Record":
                yield self.parse_record_element(element)               # get the element
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
    ) -> HealthRecord:
        attrs = element.attrib
        value = attrs.get("value")

        return HealthRecord(
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
