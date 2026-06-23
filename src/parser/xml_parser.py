from bs4 import BeautifulSoup
from .base_parser import BaseParser
from pathlib import Path


class XMLParser(BaseParser):
    def get_beautiful_soup_object(self, file: Path) -> BeautifulSoup:
        content = file.read_text(encoding="utf-8")
        return BeautifulSoup(content, "xml")

    def generate_documents(self,) -> None:
        ...