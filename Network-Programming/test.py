import socket
import time

def server():
    port = ('127.0.0.1',80)
    listener = socket.socket()
    listener.bind(port)
    listener.listen(5)
    con,addr = listener.accept()
    print('Connect succeed')
    Connection(con)

def Connection(con):
    while True:
        recv = con.recv(65535)
        print(recv)

if __name__ == '__main__':
    server()
    