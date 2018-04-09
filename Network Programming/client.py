import socket
import time

def client():
    addr = ('127.0.0.1',33333)
    con = socket.socket()
    con.connect(addr)
    con.send(b'hello\n')
    con.send(b'ack\n')
    con.send(b'bye\n')
    con.send(b'ack')
    con.close()

if __name__ == '__main__':
    client()