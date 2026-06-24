
from pathlib import Path
from parsers import Streamer


def test_stream_record_elements_returns_records_only():
    xml_parser = Streamer()
    file_path = Path(__file__).parents[1] / "fixtures" / "xml" / "small_exports.xml"
    
    itterator = xml_parser.stream_records_elements(xml_file=file_path)
    
    for element in itterator:
        assert element != "Records", f"the element have a tag {element.tag}"