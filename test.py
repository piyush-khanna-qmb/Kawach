import socket

# Define the module's IP and port
MODULE_IP = '192.168.0.100'
MODULE_PORT = 12345

# Create a socket connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((MODULE_IP, MODULE_PORT))
    # Send the command to set the upload interval (e.g., 60 seconds)
    s.sendall(b'AT+UPLOADINTERVAL=60\r\n')
    # Receive response if necessary
    response = s.recv(1024)
    print('Response:', response.decode())