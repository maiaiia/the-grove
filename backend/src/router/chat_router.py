from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse
from backend.src.service.chat_service import manager, save_message, get_recent_messages
from backend.src.service.auth_service import AuthService
from backend.src.model.database import SessionLocal

router = APIRouter()


def get_user_from_token(token: str):
    db = SessionLocal()
    try:
        auth_service = AuthService(db)
        return auth_service.get_current_user(token)
    finally:
        db.close()


@router.get("/api/chat/history")
async def chat_history():
    messages = await get_recent_messages()
    return JSONResponse(content=messages)


@router.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket, token: str=Query(None)):
    if not token:
        token = websocket.cookies.get("access_token")
        #await websocket.close(code=1008)
        #return

    if not token:
        print("DEBUG: No token found in query params or cookies")
        await websocket.close(code=1008, reason="No authentication token")
        return

    print(f"DEBUG: Token received: {token[:20]}...")  # Print first 20 chars for debugging

    user = get_user_from_token(token)
    if not user:
        await websocket.close(code=1008, reason="Invalid authentication token expired")
        return

    username = user.username
    await manager.connect(websocket, username)

    await manager.broadcast({
        "type": "system",
        "text": f"{username} joined the chat",
        "username": "system",
        "timestamp": "",
        "onlineUsers": manager.get_online_users()
    })

    try:
        while True:
            text = await websocket.receive_text()
            if not text.strip():
                continue

            message = await save_message(username, text)
            message["type"] = "message"
            message["onlineUsers"] = manager.get_online_users()
            await manager.broadcast(message)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({
            "type": "system",
            "text": f"{username} left the chat",
            "username": "system",
            "timestamp": "",
            "onlineUsers": manager.get_online_users()
        })