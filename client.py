import socket
import select
import threading

HEADER = 64
PORT = 6080
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
NICK_MESSAGE = "!NICK"
SERVER = socket.gethostbyname(
    socket.gethostname()
)  # input("IP of server you would like to connect to: ") if this is going to be run on multiple computers
ADDR = (SERVER, PORT)


def sendM(msg):
    # Encode message
    message = msg.encode(FORMAT)

    # Setup header (message length)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    # Send header, follwed by actual message
    server.send(send_length)
    server.send(message)

    # Output the message you just sent
    print(f"[YOU] {msg}")


def sendLoop():
    global server

    # Infinitely look for outgoing messages
    while True:
        msg = input("What would you like to say: ")
        sendM(msg)


def recieve():
    global server

    # Infintely look for incoming messages
    while True:
        read_sockets, write_socket, error_socket = select.select(
            [
                server,
            ],
            [],
            [],
        )

        for socks in read_sockets:
            # if message coming from server
            if socks == server:
                message = socks.recv(2048)
                print(f"\n{message.decode(FORMAT)}", end="")
                print("\nWhat would you like to say: ", end="")


def start():
    global server

    # connect to server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(ADDR)

    # Set nickname
    nick = input("What would you like your nickname to be: ")
    msg = f"{NICK_MESSAGE} {nick}"
    sendM(msg)
    print(f"Your nickname has been successfully changed to {nick}")

    # Start send loop
    sendThread = threading.Thread(target=sendLoop)
    sendThread.start()

    # Start recieve loop
    recvThread = threading.Thread(target=recieve)
    recvThread.start()


if __name__ == "__main__":
    server = None
    start()
