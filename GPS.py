import socket
from threading import Thread
import time

HOST = '10.5.48.29'  # Listen on all network interfaces
PORT = 8085
BUFSIZ = 10240
ADDR = (HOST, PORT)

print(socket.gethostname())

def accept_incoming_connections():
    while True:
        client_socket, client_address = SERVER.accept()
        print(f"Connection from {client_address}")
        Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    try: 
        while True:
            data = client_socket.recv(BUFSIZ)
            if not data:
                break
            print("Received data:", data.decode('utf-8'))
            print(time.time(), "Raw data:", data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)
SERVER.listen(5)
print(f"Server listening on {HOST}:{PORT}")

if __name__ == '__main__':
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
