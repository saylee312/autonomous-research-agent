from pymongo import MongoClient

from backend.core.config import settings


class LazyDatabase:
    def __init__(self):
        self._client = None
        self._db = None

    def _connect(self):
        if self._client is None:
            self._client = MongoClient(
                settings.MONGO_URI,
                serverSelectionTimeoutMS=5000,
            )
            self._db = self._client[settings.DB_NAME]
        return self._db

    def __getattr__(self, name):
        return getattr(self._connect(), name)

    def __getitem__(self, key):
        return self._connect()[key]


db = LazyDatabase()