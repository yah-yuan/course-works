'''
ping程序的reply程序
作者:张庭源
创建日期:Mon May 28 18:41:17 CST 2018
说明:
这是ping程序的reply部副,回应icmp echo请求
工作原理监听--回复
此程序可运行于虚拟机中,代替linux内核的网络部分
使用route del命令将默认路由表删除,可以使主机不回应ping请求
从宿主机ping虚拟机进行测试
'''

import socket
from ping_icmp import *
import os
import signal

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    signal.signal(signal.SIGINT,quit)
    while True:
        ip_recv = s.recvfrom(2048)
        ip_pack = ip_recv[0]
        ip_addr = ip_recv[1]
        icmp_dic = icmp_unpack(ip_pack)
        if icmp_dic['type'] != 8:
            continue
        elif icmp_dic['code'] != 0:
            continue
        send_pack = icmp_pack(0,icmp_dic['id'],icmp_dic['seq'],icmp_dic['data'])
        s.sendto(send_pack,ip_addr)
def quit(a,b):
    os._exit(0)


if __name__ == '__main__':
    main()