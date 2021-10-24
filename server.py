import socket
import threading

HEADER = 64
PORT = 6080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
NICK_MESSAGE = "!NICK"

list_of_clients = []
client_nicks = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def broadcast(message, conn):
    # Loop through clients
    for client in list_of_clients:
        # Only send to clients if they are not the sender
        if client != conn:
            try:
                # Send to client
                client.send(message.encode(FORMAT))
            except:
                # If link is broken remove the client
                client.close()
                remove(client)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        try:
            # First recieve the 64 byte long header
            # Header contains the length of the actual message, padded to be 64 bytes
            msg_length = conn.recv(HEADER).decode(FORMAT)

            # Only do this if the message length is not None.
            if msg_length:
                msg_length = int(msg_length)

                # Recieve the actual message
                msg = conn.recv(msg_length).decode(FORMAT)

                # Check if user wants to disconnected
                if msg == DISCONNECT_MESSAGE:
                    connected = False

                # Check if user wants to change their nickname
                if NICK_MESSAGE in msg:
                    print("received nick")
                    client_nicks[str(conn)] = msg[6 : len(msg)]

                # Create output message
                msg = f"[{client_nicks.get(str(conn))}] {msg}"
                print(msg)

                # Broadcast the output message to all the other clients
                broadcast(msg, conn)
        except:
            # If keyboard interrupt cleanly close the server
            server.close()
            exit(0)

    conn.close()


def start():
    # Start listening for new connections
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    # infinitely check for new connections
    while True:
        try:
            # Accept new connections
            conn, addr = server.accept()

            # Add client to a list and add their nickname to a dictionary
            list_of_clients.append(conn)
            client_nicks[str(conn)] = addr

            # Open a thread to handle messages to and from this client
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        except:
            # If keyboard interrupt cleanly close the server
            server.close()
            exit(0)

    conn.close()
    server.close()


if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()
