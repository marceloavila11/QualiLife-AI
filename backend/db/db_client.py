import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

if not MONGO_URI or not MONGO_DB:
    raise RuntimeError("Faltan variables MONGO_URI o MONGO_DB en .env")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
