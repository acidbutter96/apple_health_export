import xml.etree.ElementTree as ET

from collections import Counter
from pathlib import Path


class Profiler:
    def profile_xml(self, xml_file: Path) -> dict[str, dict[str, int]]:
        tag_counter: Counter[str] = Counter()
        record_type_counter: Counter[str] = Counter()

        context = ET.iterparse(source=xml_file, events=("end",))

        for _, element in context:
            tag = element.tag
            tag_counter[tag] += 1

            if tag == "Record":
                record_type = element.attrib.get("type", "<missing>")
                record_type_counter[record_type] += 1
            element.clear()
        return {
            "tag_counts": dict(tag_counter),
            "record_type_counts": dict(record_type_counter)
        }