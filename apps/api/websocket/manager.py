from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, request_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[request_id] = websocket

    def disconnect(self, request_id: str):
        if request_id in self.active_connections:
            del self.active_connections[request_id]

    async def send_result(self, request_id: str, data: dict):
        websocket = self.active_connections.get(request_id)
        if websocket:
            await websocket.send_json(data)

manager = ConnectionManager()