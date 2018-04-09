import socket
import time

def client():
    addr = ('127.0.0.1',33334)
    con = socket.socket()
    con.connect(addr)
    while True:
        con.send(b'Hey There!')
        time.sleep(0.5)

if __name__ == '__main__':
    client()