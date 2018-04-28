import socket
import time

def server():
    port = ('127.0.0.1',33333)
    listener = socket.socket()
    listener.bind(port)
    listener.listen(5)
    con,addr = listener.accept()
    print('Connect succeed')
    Connection(con)

def Connection(con):
    while True:
        recv = con.recv(65535)
        if recv == b'':
            print('Remote closed')
            break
        elif b'hello syn' in recv:
            print(recv.decode('utf8'))
            con.send(b'ack syn')
        elif b'fin' in recv:
            print(recv.decode('utf8'))
            con.send(b'ack')
            con.send(b'fin')
        elif b'hello ack' in recv:
            print(recv.decode('utf8'))
        elif b'ack' in recv:
            print(recv.decode('utf8'))
            con.close()
            break
        else:
            print(recv.decode('utf8'))

if __name__ == '__main__':
    server()
    