import xml.etree.ElementTree as ET

from collections.abc import Iterator
from pathlib import Path

from app.models.health_record_model import HealthRecord, HealthRecordEvent
from app.parsers.parser_base import ParserBase


class XMLParser(ParserBase):
    """Streaming parser for Apple Health `export.xml` files."""

    def stream_records_elements(self, xml_file: Path) -> Iterator[HealthRecord]:
        """Yield parsed HealthRecord objects one by one.

        The method uses ElementTree.iterparse with the `end` event, because at
        the end of a Record element all attributes and child MetadataEntry values
        are available.
        """
        context = ET.iterparse(source=xml_file, events=("end",))
        record_index = 0

        for _, element in context:
            tag = self._clean_tag(element.tag)

            if tag == "Record":
                record_index += 1
                yield self.parse_record_element(
                    element=element,
                    record_index=record_index,
                )
                element.clear()
                continue

            # Do not clear MetadataEntry before the parent Record is parsed.
            # Otherwise, a Record with metadata could lose its child attributes.
            if tag != "MetadataEntry":
                element.clear()

    def stream_record_events(
        self,
        xml_file: Path,
        run_id: int,
    ) -> Iterator[HealthRecordEvent]:
        """Yield HealthRecordEvent objects linked to a parse run."""
        for record in self.stream_records_elements(xml_file):
            yield HealthRecordEvent(run_id=run_id, health_record=record)

    def metadata_parser(self, element: ET.Element) -> dict[str, str]:
        """Parse MetadataEntry children from a Record element."""
        metadata: dict[str, str] = {}

        for child in element:
            child_tag = self._clean_tag(child.tag)
            if child_tag != "MetadataEntry":
                continue

            key = child.attrib.get("key")
            value = child.attrib.get("value")

            if key is not None and value is not None:
                metadata[key] = value

        return metadata

    def parse_record_element(
        self,
        element: ET.Element,
        record_index: int | None = None,
    ) -> HealthRecord:
        """Convert one XML Record element into a HealthRecord dataclass."""
        attrs = element.attrib
        value = attrs.get("value")

        record = HealthRecord(
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
            export_record_index=record_index,
            metadata=self.metadata_parser(element),
        )
        record.record_hash = self.compute_record_hash(record)
        return record
