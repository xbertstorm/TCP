import asyncio
import websockets
import json

async def handle_client(websocket, path):
    print(f"有客戶端連線進來: {websocket.remote_address}")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)

                if "Test" in data.get("Action", ""):
                    await asyncio.sleep(3)
                    response = {"Status": "Success"}
                    await websocket.send(json.dumps(response))
                elif "Unicorn" in data.get("Action", ""):
                    await asyncio.sleep(3)
                    response = {"Status": "Error"}
                    await websocket.send(json.dumps(response))
            except json.JSONDecodeError:
                print("收到非 JSON 格式資料")
            except Exception as e:
                print(f"資料處理錯誤: {e}")
    except websockets.exceptions.ConnectionClosed:
        print("📴 客戶端已斷線")
    except Exception as e:
        print(f"WebSocket 錯誤: {e}")

async def start_server():
    print("啟動 WebSocket 伺服器，等待連線中...")
    async with websockets.serve(handle_client, "0.0.0.0", os.getenv("PORT")):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(start_server())
