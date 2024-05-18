from abc import ABC, abstractmethod
from pathlib import Path


class FileGetter(ABC):
    def __init__(self, folder_name: str):
        """
        :param folder_name: src -> folder_name
        """
        self.__root_folder = Path(__file__).parent.parent
        self._folder_name = self.__root_folder / folder_name

    def get_filepath(self, filename: str, root_path: Path = None) -> Path | None:
        if root_path is None:
            root_path = self._folder_name

        filepath = root_path / filename
        if not filepath.exists():
            raise FileNotFoundError(filepath)

        if filepath.is_dir():
            for path in filepath.iterdir():
                return self.get_filepath(filename, path)
            return None
        return filepath
