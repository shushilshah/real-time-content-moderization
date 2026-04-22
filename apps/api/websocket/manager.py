from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.pending_results: Dict[str, dict] = {}  # for handling result lost when user is late

    async def connect(self, request_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[request_id] = websocket
        print(f"Connected: {request_id}")

        # if result is already exists -> send immediately
        if request_id in self.pending_results:
            print(f"Sending buffered result: {request_id}")
            await websocket.send_json(self.pending_results[request_id])
            del self.pending_results[request_id]


    def disconnect(self, request_id: str):
        self.active_connections.pop(request_id, None)
        # if request_id in self.active_connections:
        #     del self.active_connections[request_id]

    async def send_result(self, request_id: str, data: dict):
        websocket = self.active_connections.get(request_id)
        if websocket:
            print(f"Sending live: {request_id}")
            await websocket.send_json(data)
        else:
            print(f"Storing for later: {request_id}")
            self.pending_results[request_id] = data

manager = ConnectionManager()