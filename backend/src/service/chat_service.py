from fastapi import WebSocket
from datetime import datetime, timezone
from backend.src.model.mongodb import get_messages_collection


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[dict] = []

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append({
            "websocket": websocket,
            "username": username
        })

    def disconnect(self, websocket: WebSocket):
        self.active_connections = [
            c for c in self.active_connections
            if c["websocket"] != websocket
        ]

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection["websocket"].send_json(message)
            except Exception:
                disconnected.append(connection)
        for c in disconnected:
            self.active_connections.remove(c)

    def get_online_users(self) -> list[str]:
        return [c["username"] for c in self.active_connections]


manager = ConnectionManager()


async def save_message(username: str, text: str) -> dict:
    collection = get_messages_collection()
    message = {
        "username": username,
        "text": text,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    result = await collection.insert_one(message)
    message["id"] = str(result.inserted_id)
    message.pop("_id", None)
    return message


async def get_recent_messages(limit: int = 50) -> list[dict]:
    collection = get_messages_collection()
    cursor = collection.find({}).sort("timestamp", -1).limit(limit)
    messages = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        messages.append(doc)
    messages.reverse()
    return messages