import socket
import time

def client():
    addr = ('127.0.0.1',6666)
    con = socket.socket()
    con.connect(addr)
    while True:
        con.send('88::88')
        time.sleep(1)

if __name__ == '__main__':
    client()
