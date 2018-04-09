import socket

def server():
    port = ('127.0.0.1',33334)
    listener = socket.socket()
    listener.bind(port)
    listener.listen(5)
    con,addr = listener.accept()
    print('Connect succeed')
    Connection(con)

def Connection(con):
    con.
    while True:
        recv = con.recv(65535)
        if recv == b'':
            print('Remote closed')
            break
        else:
            print(recv.decode('utf8'))

if __name__ == '__main__':
    server()
    