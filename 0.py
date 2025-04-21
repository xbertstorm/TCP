import socket
import time
import json

server_socket = None
client_socket = None
client_address = None
running = False

def start_server():
    global server_socket, running
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", 12345))
        server_socket.listen(1)
        print("伺服器啟動，等待客戶端連線...\n")
        running = True
        wait_for_client()
    except Exception as e:
        print(f"伺服器啟動失敗: {e}")
        stop_server()

def wait_for_client():
    global client_socket, client_address
    server_socket.setblocking(False)

    while running:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"客戶端已連線：{client_address}\n")
            check_client_messages()
        except BlockingIOError:
            time.sleep(0.1)
        except Exception as e:
            print(f"等待連線時發生錯誤：{e}")
            stop_server()
            break

def check_client_messages():
    global client_socket, running
    client_socket.setblocking(False)

    while running:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if data:
                json_data = json.loads(data)

                if "Test" in json_data["Action"]:
                    time.sleep(3)
                    response = {
                        "Status" : "Success"
                    }
                    response_json_string = json.dumps(response)
                    client_socket.send(response_json_string.encode("utf-8"))
                elif "Unicorn" in json_data["Action"]:
                    time.sleep(3)
                    response = {
                        "Status" : "Error"
                    }
                    response_json_string = json.dumps(response)
                    client_socket.send(response_json_string.encode("utf-8"))

            else:
                print("客戶端已斷線")
                disconnect_client()
                break
        except BlockingIOError:
            time.sleep(0.1)
        except Exception as e:
            print(f"接收錯誤：{e}")
            disconnect_client()
            break

def disconnect_client():
    global client_socket
    if client_socket:
        client_socket.close()
        client_socket = None
        print("📴 客戶端已斷線，等待新的連線...\n")

def stop_server():
    global server_socket, client_socket, running
    running = False

    if client_socket:
        client_socket.close()
        client_socket = None

    if server_socket:
        server_socket.close()
        server_socket = None

    print("伺服器已關閉")

if __name__ == "__main__":
    start_server()
