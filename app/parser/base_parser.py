from pathlib import Path


class BaseParser:
    def __init__(
        self,
        data_path: Path | str = "",
        output_format : str = "",
    ):
        self.data_path: Path = (
            Path(data_path or self._get_data_path)
        ).resolve(strict=True,)
        self.output_format: str = output_format or ".csv"

    def generate_data_dict(
        self,
        path: Path,
        data: dict[str, list[str]] | None = None,
    ) -> dict[str, list[str]]:
        if data is None:
            data = {
                "xml": [],
                "gpx": [],
            }

        if not path.is_dir():
            return data

        for file in path.iterdir():
            if file.name == ".gitkeep":
                continue

            if file.is_file():
                file_suffix = file.suffix[1:].lower()

                if file_suffix in data:
                    data[file_suffix].append(str(file.resolve()))

            elif file.is_dir():
                self.generate_data_dict(path=file, data=data)

        return data

    def get_data_dict(self,) -> dict[str, list[str]] | dict:
        data_dict = self.generate_data_dict(path=self.data_path)
        data_dict = {
            "health": data_dict.get("xml", []),
            "workout-routes": data_dict.get("gpx", [])
        }
        return data_dict

    @property
    def _get_data_path(self,) -> str:
        return str(Path().cwd().resolve() / "data")