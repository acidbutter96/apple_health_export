import xml.etree.ElementTree as ET

from collections import Counter
from pathlib import Path
from typing import TypedDict

from app.parsers.parser_base import ParserBase


class XMLProfile(TypedDict):
    tags_counter: Counter[str]
    tags_types_counters: dict[str, Counter[str]]


class XMLProfileParser(ParserBase):
    """Streaming profiler for large XML files.

    Chapter 3 focuses on profiling: count tags and optionally count the `type`
    attribute for selected tags such as Record.
    """

    def __init__(
        self,
        xml_path: Path | None = None,
        tags_to_profile: list[str] | set[str] | None = None,
    ) -> None:
        self.xml_counts: XMLProfile | None = None

        if xml_path is not None:
            self.profile_xml(
                xml_file=xml_path,
                tags_to_profile=tags_to_profile,
            )

    def profile_xml(
        self,
        xml_file: Path,
        tags_to_profile: list[str] | set[str] | None = None,
    ) -> XMLProfile:
        tags_to_profile_set = set(tags_to_profile or [])

        tags_counter: Counter[str] = Counter()
        tags_types_counter_dict: dict[str, Counter[str]] = {}

        context = ET.iterparse(source=xml_file, events=("end",))

        for _, element in context:
            element_tag = self._clean_tag(element.tag)
            tags_counter[element_tag] += 1

            if not tags_to_profile_set or element_tag in tags_to_profile_set:
                element_type = element.attrib.get("type", "<missing>")
                tags_types_counter_dict.setdefault(element_tag, Counter())
                tags_types_counter_dict[element_tag][element_type] += 1

            element.clear()

        self.xml_counts = {
            "tags_counter": tags_counter,
            "tags_types_counters": tags_types_counter_dict,
        }
        return self.xml_counts

    def profile_record_xml(self) -> dict[str, dict[str, int]]:
        if self.xml_counts is None:
            raise RuntimeError("Run profile_xml first")

        record_counter = self.xml_counts["tags_types_counters"].get(
            "Record",
            Counter(),
        )

        return {
            "tags_counter": dict(self.xml_counts["tags_counter"]),
            "record_type_counter": dict(record_counter),
        }
