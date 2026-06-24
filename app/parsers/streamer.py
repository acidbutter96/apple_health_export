import xml.etree.ElementTree as ET

from pathlib import Path
from collections.abc import Iterator


class Streamer:
    def stream_records_elements(self, xml_file: Path) -> Iterator[ET.Element]:
        context = ET.iterparse(
            source=xml_file,
            events=("end",)     # could be ignored
        )
        
        for event, element in context:      #  event says if is the start or end of the tag, element it's the tag it self
            if element.tag == "Records":
                yield element               # get the element
                "".split("")
            element.clear()                 #   relase from memory
