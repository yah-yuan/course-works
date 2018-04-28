import socket

def client():
    addr = ('127.0.0.1',33333)
    con = socket.socket()
    con.connect(addr)
    con.send(b'hello syn\n')
    recv = con.recv(65535)
    print(recv.decode('utf8'))
    con.send(b'hello ack')
    # bye
    con.send(b'fin')
    while True:
        recv = con.recv(65535)
        if recv == b'ack':
            print(recv.decode('utf8'))
            break
    recv = con.recv(65535)
    print(recv.decode('utf8'))
    con.send(b'ack')
    con.close()

if __name__ == '__main__':
    client()