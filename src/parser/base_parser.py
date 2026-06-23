from bs4 import BeautifulSoup
from pathlib import Path



class BaseParser:
    def __init__(
        self,
        data_path: Path | str = "",
        output_format : str = "",
    ):
        self.data_path: Path = (
            Path(data_path) or self.get_data_path
        ).resolve(strict=True,)
        self.output_format: str = output_format or ".csv"
    
    def check_for_files(
        self,
        path: Path,
        files_list: list[Path] = [],
    ) -> list[Path]:
        if path.is_dir():
            for file in path.iterdir():
                if file.is_file():
                    files_list.append(file.resolve())
                    continue

                if file.is_dir():
                    new_list = self.check_for_files(
                        files_list=files_list,
                        path=file,
                    )
                    files_list = [*files_list, *new_list]

        return files_list

    def get_files(self,) -> list[Path] | list:
        return self.check_for_files(path=self.data_path)
    
    @property
    def get_data_path(self,) -> Path:
        return Path("../data")