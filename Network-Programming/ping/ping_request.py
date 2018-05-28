'''
ping程序的request程序
作者:张庭源
创建日期:Mon May 28 09:33:00 CST 2018
说明:
这是ping程序的Request程序
主要逻辑有请求包发送和回显包解析两个部分
icmp包的构造和解析包含在ping_icmp.py中
'''

import os
import signal
import socket
import sys  # 获取命令行参数
import threading
import time

from ping_icmp import *


def is_ip_addr(addr):
    '''判断是否是一个ip地址'''
    item_list = addr.split('.')
    if not len(item_list) == 4:
        return False
    try:
        for i in range(len(item_list)):
            item_list[i] = int(item_list[i])
    except ValueError:
        return False
    for item in item_list:
        if not 0 < item < 255:
            return False
    return True


class pack_pool(object):
    '''将包信息存入字典'''

    def __init__(self):
        self.pingstart = time.time()
        self.current_seq = 0
        self.packlist = {}

    def get_new_pack(self):
        seq = self.current_seq
        self.current_seq += 1
        pack = icmp_pack(8, seq)
        info = pack_info()
        self.packlist[seq] = info
        return pack

    def recv_pack(self, seq):
        try:
            info = self.packlist[seq]
        except KeyError:
            print('got a seq which was not send by this PING')
        info.get_reply()
        return info.TTL

    def summary(self, signum, frame):
        print('\n-------------------------------')
        print('\t    Summary')
        print('-------------------------------')
        length = len(self.packlist)
        pingend = time.time()
        loss_count = 0
        totalTTL = 0
        for i in range(length):
            info = self.packlist[i]
            if not info.replied:
                loss_count += 1
            else:
                totalTTL += info.TTL

        recv = length - loss_count
        if recv:
            avgTTL = totalTTL / (length - loss_count)
        else:
            avgTTL = None
        pack_loss_rate = loss_count / length
        pingtime = pingend - self.pingstart
        print('Send packets:', length)
        print('Get replied:', recv)
        print('Packet loss:', pack_loss_rate * 100, '\b%')
        if recv:
            print('avgTTL:', round(avgTTL * 1000, 2), 'ms')
        print('PING run time:', round(pingtime, 2), '\bs')
        os._exit(0)


class pack_info(object):
    '''创建发送包的信息'''

    def __init__(self):
        self.replied = False  # 没收到回复
        self.timeofsend = time.time()
        self.timeofrecv = 0
        self.TTL = 0

    def get_reply(self):
        self.replied = True
        self.timeofrecv = time.time()
        self.TTL = self.timeofrecv - self.timeofsend


def main(argv):
    '''分析地址 创建监听线程 创建发送线程'''
    if len(argv) > 1:
        address = argv[1]
    else:
        print('help')
        sys.exit()

    domain = ''
    if not is_ip_addr(address):
        domain = address
        address = socket.gethostbyname(address)
    if domain:
        print('Now ping to', address, '(', domain, ')')
    else:
        print('Now ping to', address)

    pool = pack_pool()
    signal.signal(signal.SIGINT, pool.summary)

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    recving = threading.Thread(target=recv, args=(pool, s))
    sending = threading.Thread(target=send, args=(pool, s, address))

    sending.start()
    recving.start()

    sending.join()
    recving.join()


def send(pool, sock, addr):
    while True:
        pack = pool.get_new_pack()
        sock.sendto(pack, (addr, 0))
        # print('Now sending', pool.current_seq - 1, 'of pack')
        time.sleep(1)


def recv(pool, sock):
    while True:
        pid = os.getpid()
        pack = sock.recvfrom(2048)
        fromip = pack[1][0]
        msg = icmp_unpack(pack[0])
        # 测试type和code是否正确
        if not (msg['type'] == 0 and msg['code'] == 0):
            print('recv icmp pack from', fromip,
                  ', but icmp type or code incorrect!!')
            continue
        # 查看pid是否为本进程
        if msg['id'] != pid:
            print('recv icmp pack from', fromip,
                  ', but current icmp is not for this PING!!')
            continue
        seq = msg['seq']
        data = msg['data']
        TTL = pool.recv_pack(seq)
        print('recv icmp pack from', fromip, ', seq=', seq, ', TTL=',
              round(TTL * 1000, 2), 'ms, data=', data)


if __name__ == '__main__':
    argv = sys.argv
    main(argv)
