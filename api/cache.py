from typing import Any, Dict
from config import Config


class DictionaryCache:
    cache: Dict[str, Any]
    prefix: str

    def __init__(self, prefix: str = "") -> None:
        self.cache = {}
        self.prefix = prefix

    def get(self, key: str) -> Any:
        """Retrieve data according to key

        Args:
            key (str): Key name

        Returns:
            Any: stored value, None if not exist
        """
        return self.cache.get(f"{self.prefix}_{key}", None)

    def set(self, key: str, value: Any) -> None:
        """Set data according to key

        Args:
            key (str): Key name
            value (Any): value
        """
        if Config.MOCK_RESPONSE:
            self.cache[f"{self.prefix}_{key}:latest"] = value
        self.cache[f"{self.prefix}_{key}"] = value

    def delete(self, key: str) -> None:
        """Delete data according to key

        Args:
            key (str): Key name
        """
        if f"{self.prefix}_{key}" in self.cache:
            del self.cache[f"{self.prefix}_{key}"]
