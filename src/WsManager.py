from typing import Dict

from fastapi import WebSocket

class WsManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, key: str):
        await websocket.accept()
        self.active_connections[key] = websocket

    def disconnect(self,key:str):
        self.active_connections[key].close()
        del self.active_connections[key]

    async def send_text(self, message: str,key:str):
        await self.active_connections[key].send_text(message)
