from pathlib import Path

def test_stream_record_elements_returns_records_only(tests_directory_path: Path):
    path = tests_directory_path
    print(path)
    assert False, str(path)