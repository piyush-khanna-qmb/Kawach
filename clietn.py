import socket

# Define server details
SERVER_DNS = 'localhost'  # Replace with your server's DNS name
SERVER_PORT = 8085  # Replace with your server's port number
BUFFER_SIZE = 4096

def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((SERVER_DNS, SERVER_PORT))
        print(f"Connected to server at {SERVER_DNS}:{SERVER_PORT}")

        # Send a test message
        message = "Hello, Server! This is a test message."
        client_socket.sendall(message.encode('utf-8'))
        print("Message sent:", message)
        
        # Receive a response from the server
        response = client_socket.recv(BUFFER_SIZE)
        print("Received response from server:", response.decode('utf-8'))
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the connection
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    main()
