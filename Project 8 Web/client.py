# Client program
import socket

host = input("Host IP (10.13.37.69):")
port = int(input("Host port (e.g. 8080):"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    while True:
        msg = input("> ")
        s.sendall(msg.encode())
        data = s.recv(1024)
        print("<", repr(data))

