import socket
s = socket.socket()
ip = socket.gethostbyname('www.baidu.com')
s.connect((ip,80))
head = ''''GET / HTTP/1.1\r
Host: '''+ip+':'+'80'+'''\r
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r
Accept-Language: en-GB,en;q=0.5\r
Accept-Encoding: gzip, deflate\r
Connection: keep-alive\r
Upgrade-Insecure-Requests: 1'''
s.send(head.encode('utf8'))
recv = s.recv(65535)
print(recv.decode('utf8'))