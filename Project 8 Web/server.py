# Server
import socket

host = ''  # '' means all interfaces                
port = int(input("Listen port (e.g. 8080):"))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((host,port))
    s.listen(1)
    print("Server started, waiting for incoming connection")
    conn, addr = s.accept()


    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print("< ", repr(data))
            msg = input("> ")
            conn.sendall(msg.encode())
