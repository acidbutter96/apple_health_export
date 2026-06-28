from argparse import ArgumentParser
from pathlib import Path

from app.database.connection import get_connection
from app.pipeline.ingestion import IngestionPipeline


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="Apple Health Export")
    parser.add_argument(
        "xml_file",
        type=Path,
        help="Path to the Apple Health export.xml file.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1_000,
        help="Number of parsed records to insert per database batch.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    with get_connection() as connection:
        pipeline = IngestionPipeline(connection=connection, batch_size=args.batch_size)
        result = pipeline.ingest_xml(args.xml_file)

    print(result)


if __name__ == "__main__":
    main()
