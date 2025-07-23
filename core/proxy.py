import socket
import threading

LOCAL_HOST = '0.0.0.0'     # Listen on all interfaces
LOCAL_PORT = 8080          # Expose this port on Wi-Fi
TARGET_HOST = '127.0.0.1'  # Django running here
TARGET_PORT = 8000

def handle_client(client_socket):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_socket:
        remote_socket.connect((TARGET_HOST, TARGET_PORT))
        threading.Thread(target=forward, args=(client_socket, remote_socket)).start()
        forward(remote_socket, client_socket)

def forward(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            print(f"Forwarding {len(data)} bytes")
            destination.sendall(data)
    except Exception as e:
        print(f"Forwarding error: {e}")
    finally:
        source.close()
        destination.close()


def start_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LOCAL_HOST, LOCAL_PORT))
        server.listen(5)
        print(f"Proxy server listening on {LOCAL_HOST}:{LOCAL_PORT}")
        
        while True:
            client_sock, addr = server.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=handle_client, args=(client_sock,)).start()

if __name__ == '__main__':
    start_proxy()
