from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from apps.api.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws/{request_id}")
async def websocket_endpoint(websocket: WebSocket, request_id: str):
    await manager.connect(request_id, websocket)

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        manager.disconnect(request_id)