from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

        async def connect(self, websocket: WebSocket, user_id: str):
            await websocket.accept()
            if user_id not in self.active_connections:
                self.active_connections[user_id] = []
                self.active_connections[user_id].append(websocket)

        async def disconnect(self, websocket: WebSocket, user_id: str):
            if user_id in self.active_connections:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

        async def send_message(self, message: str, user_id: str):
            if user_id in self.active_connections:
                for connection in self.active_connections:
                    await connection.send_text(message)


manager = ConnectionManager()
