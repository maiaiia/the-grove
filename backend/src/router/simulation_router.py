from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.src.service import simulation_service

simulation_router = APIRouter(prefix="/api/simulation", tags=["simulation"])

@simulation_router.post("/start")
async def start_simulation():
    simulation_service.start()
    return {"status": "started"}

@simulation_router.post("/stop")
async def stop_simulation():
    simulation_service.stop()
    return {"status": "stopped"}

@simulation_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    simulation_service.register(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        simulation_service.unregister(websocket)