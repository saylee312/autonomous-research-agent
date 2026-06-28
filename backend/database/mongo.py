from pymongo import MongoClient

from backend.core.config import settings


client = MongoClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=5000
)

client.admin.command("ping")

db = client[settings.DB_NAME]