from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from src.WsManager import WsManager
from src.models import Datas
import json
# from src.filter import filter

manager = WsManager()
# filters = filter()
app = FastAPI()

key_store = {}

class Counter():
    counter =  0
    
    def getCount(self):
        self.counter+=1
        return self.counter
    
counter = Counter()

# CORSの設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可する場合
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可 (GET, POSTなど)
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

@app.get("/")
async def get():
    return HTMLResponse("Hello POS System")

@app.get("/api/key/{key}")
#keyのエンドポイント
async def api_endpoint(key: str):
    #countに1プラスする関数
    id_ = counter.getCount()
    key_store[key] = id_
    await manager.send_text(json.dumps({"status": "payed", "id": id_}),key)
    manager.disconnect(key)
    return {"status": "payed", "id": id_}

@app.websocket("/ws/{key}")
async def websocket_endpoint(websocket: WebSocket,key:str):
    await manager.connect(websocket,key)
    try:
        while True:
            key = await websocket.receive_text()
            #keyだけ送られたとき
            key_store[key] = None
            await websocket.send_text(json.dumps({"status": "waiting"}))
    except WebSocketDisconnect:
        #接続が切れた場合は削除
        manager.disconnect(key)
        #keyの削除
        print(f"remove key: {key}")
        del key_store[key]
    