from pathlib import Path


class DB:
    def __init__(self, path: Path | str):
        # should I use ctypes?
        pass

    def get_int(self, key: str, fail: None | int):
        return None

    def save_int(self, key: str, value: int):
        pass

    def get(self, key: str, fail: str | None):
        pass

    def save(self, key: str, val: str):
        pass
