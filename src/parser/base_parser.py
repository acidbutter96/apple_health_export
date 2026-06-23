from pathlib import Path


class BaseParser:
    def __init__(
        self,
        data_path: Path | str = "",
        output_format : str = "",
    ):
        self.data_path: Path = (
            Path(data_path) or self._get_data_path
        ).resolve(strict=True,)
        self.output_format: str = output_format or ".csv"

    def generate_data_dict(
        self,
        path: Path,
        data: dict[str, list[Path]] = {},
    ) -> dict[str, list[Path]]:
        data_list: dict[str, list[Path]] = data or {
            "xml": [],
            "gpx": [] 
        }
        if path.is_dir():
            for file in path.iterdir():
                not_gitkeep: bool = file.name != ".gitkeep"
                if file.is_file() and not_gitkeep:
                    file_suffix = file.suffix[1:].lower() or ""
                    data_list.get(file_suffix, []).append(file)

                    continue

                new_data_dict: dict[str, list[Path]]= {}
                if file.is_dir() and not_gitkeep:
                    new_data_dict = {
                        **self.generate_data_dict(
                                data=data,
                                path=file,
                            )
                        }
                    data = {
                        **data,
                        **new_data_dict,
                    }

        return data_list

    def get_data_dict(self,) -> dict[str, list[Path]] | dict:
        return self.generate_data_dict(path=self.data_path)

    @property
    def _get_data_path(self,) -> Path:
        return Path("../data")