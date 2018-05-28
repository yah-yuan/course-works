'''
ping程序的icmp打包库
作者:张庭源
创建日期:Mon May 28 09:12:32 CST 2018
说明:
这是ping程序的icmp包打包库
提供的打包和解包功能被ping_request和ping_reply调用
解包功能会监测checksum的正确性
'''
import os
import socket
import sys
from struct import *


def carry_around_add(a, b):
    '反码求和'
    c = a + b
    return (c & 0xffff) + ((c >> 16) & 0xffff)


def checksum(msg):
    '''计算包的校验和'''
    if len(msg) % 2 != 0:  #补全
        msg += '\0'
    s = 0
    for i in range(0, len(msg), 2):
        w = ((msg[i] << 8) & 0xffff) + (msg[i + 1] & 0xff)
        s = carry_around_add(s, w)
    cksum = ~s & 0xffff
    return cksum


def icmp_pack(type, sequence):
    '''type = 0     回显包
       type = 8     请求包
    '''
    icmp_type = type
    icmp_code = 0
    icmp_cksum = 0

    icmp_id = os.getpid()
    icmp_seq = sequence
    icmp_data = b'PING'

    # 按上面描述的结构，构建icmp header
    # !代表网络字节序
    icmp_pack = pack('!BBHHH4s', icmp_type, icmp_code, icmp_cksum, icmp_id,
                     icmp_seq, icmp_data)

    icmp_cksum = checksum(icmp_pack)

    icmp_pack = pack('!BBHHH4s', icmp_type, icmp_code, icmp_cksum, icmp_id,
                     icmp_seq, icmp_data)
    # 最终的 icmp packet
    return icmp_pack


def icmp_unpack(raw_pack):
    '''解包,返回一个{字段:数据}的字典'''
    raw_pack = raw_pack[20:32]
    msg = unpack('!BBHHH4s', raw_pack)
    msg_dic = {
        'type': msg[0],
        'code': msg[1],
        'cksum': msg[2],
        'id': msg[3],
        'seq': msg[4],
        'data': msg[5]
    }
    # 测试cksum正确性
    check_pack = pack('!BBHHH4s', msg_dic['type'], msg_dic['code'], 0,
                      msg_dic['id'], msg_dic['seq'], msg_dic['data'])
    if checksum(check_pack) == msg_dic['cksum']:
        msg_dic['data'] = msg_dic['data'].decode('utf8')
        return msg_dic
    else:
        print('cksum error')


if __name__ == '__main__':
    icmp_pack(8, 0)
