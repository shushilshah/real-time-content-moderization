from fastapi import APIRouter
from apps.api.websocket.manager import manager

router = APIRouter()


@router.post("/internal/result")
async def push_result(data: dict):
    print("RECEIVED DATA:", data)
    request_id = data.get("request_id")
    if not request_id:
        return {"error": "request_id is missing"}

    await manager.send_result(request_id, data)
    return {"status": "sent"}
