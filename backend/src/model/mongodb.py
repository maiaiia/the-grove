from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "grove_chat")


client: AsyncIOMotorClient = None
db = None

async def connect_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGO_URL, authSource="admin")
    db = client[MONGO_DB]
    await db.messages.create_index("timestamp")
    print("Connected to MongoDB")


async def disconnect_mongo():
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")


def get_messages_collection():
    return db.messages