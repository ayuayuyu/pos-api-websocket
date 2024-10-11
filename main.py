from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from src.WsManager import WsManager
from src.models import Datas
from src.filter import filter

manager = WsManager()
filters = filter()
app = FastAPI()

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
    filters.setCount()
    filters.keys[key] = filters.getCount()
    return {"state": "payed", "id": {filters.getCount()}}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,data: Datas):
    await manager.connect(websocket)
    try:
        while True:
            datas = await websocket.receive_text()
            #keyだけ送られたとき
            if datas:
                filters.key[datas] = "null"
                print(f"dict: {filters.keys()}")
                await manager.send_text({"state": "waiting"})
            #keyとidがある時
            else:
                filters.keys[data.key] = data.id
    except WebSocketDisconnect:
        #接続が切れた場合は削除
        manager.disconnect(websocket)
        #keyの削除
        print(f"remove key: {data.key}")
        del filters.keys[data.key]