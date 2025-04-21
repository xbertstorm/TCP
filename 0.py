from websocket_server import WebsocketServer
import json
import time

def new_client(client, server):
    print(f"客戶端已連線：{client['address']}")
    server.send_message(client, json.dumps({"Status": "Connected"}))

def message_received(client, server, message):
    print(f"收到訊息：{message}")
    try:
        data = json.loads(message)

        if "Test" in data.get("Action", ""):
            time.sleep(3)
            response = {"Status": "Success"}
        elif "Unicorn" in data.get("Action", ""):
            time.sleep(3)
            response = {"Status": "Error"}
        else:
            response = {"Status": "Unknown Action"}

        server.send_message(client, json.dumps(response))

    except Exception as e:
        print(f"JSON 處理錯誤：{e}")
        server.send_message(client, json.dumps({"Status": "Invalid JSON"}))

def client_left(client, server):
    print(f"📴 客戶端已離線：{client['address']}")

PORT = 12345
server = WebsocketServer(host='0.0.0.0', port=PORT)
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.set_fn_client_left(client_left)

print("WebSocket 伺服器已啟動，等待連線中...")
server.run_forever()
