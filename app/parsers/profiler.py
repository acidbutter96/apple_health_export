import xml.etree.ElementTree as ET

from collections import Counter
from pathlib import Path
from typing import TypedDict


class XMLProfile(TypedDict):
    tags_counter: Counter[str]
    tags_types_counters: dict[str, Counter[str]]


class Profiler:
    def __init__(self, xml_path: Path):
        self.xml_counts : XMLProfile | None = None
        self.profile_xml(xml_file=xml_path)

    def _clean_tag(self, tag: str) -> str:
        if "}" in tag:
            return tag.split("}")[-1]
        return tag

    def profile_xml(
        self,
        xml_file: Path,
        tags_to_profile: list[str] | set[str] | None = None,
    ) -> XMLProfile:
        tags_to_profile = set(tags_to_profile or [])

        tags_counter: Counter[str] = Counter()
        tags_types_counter_dict: dict[str, Counter[str]] = {}

        context = ET.iterparse(source=xml_file, events=("end",))

        for _, element in context:
            element_tag = self._clean_tag(element.tag)
            tags_counter[element_tag] += 1

            if not tags_to_profile or element_tag in tags_to_profile:
                element_type = element.attrib.get("type", "<missing>")

                tags_types_counter_dict.setdefault(element_tag, Counter())
                tags_types_counter_dict[element_tag][element_type] += 1
            element.clear()

        self.xml_counts: XMLProfile = {
            "tags_counter": tags_counter,
            "tags_types_counters": tags_types_counter_dict
        }
        
        return self.xml_counts

    def profile_record_xml(self,) -> dict[str, dict[str, int]]:
        if not self.xml_counts:
            raise RuntimeError("Run profile_xml first")

        record_counter: Counter[str] = (
            self.xml_counts["tags_types_counters"].get("Record", Counter(""))
        )

        return {
            "tags_counter": dict(self.xml_counts["tags_counter"]),
            "record_type_counter": dict(record_counter)
        }
