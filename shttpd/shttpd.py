
import argparse
import configparser
import datetime
import multiprocessing
import os
import socket
import sys
import threading
import time

import prettytable


class Request(object):
    status = 0
    status_code = 0
    is_dir = 0
    is_cgi_file = 0
    is_html_file = 0
    path = ''
    cgi_param = []
    http_type = ''
    is_src_file = 0


def _param():
    '''解析程序参数'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--configFile', help='Set the config file path,by default=./config',
                        dest='configFile', default='./config')
    parser.add_argument('-C', '--CGIpath',
                        help='Set the CGI file path', dest='CGIpath')
    parser.add_argument('-w', '--wwwpath',
                        help='Set the web file path', dest='wwwpath')
    parser.add_argument('-d', '--default',
                        help='Set default page', dest='default')
    parser.add_argument('-t', '--TimeOut',
                        help='Set time out', type=int, dest='TimeOut')
    parser.add_argument(
        '-p', '--port', help='Set the working port of server', type=int, dest='port')
    parser.add_argument(
        '-m', '--MaxClient', help='Set the maximum of client connection', type=int, dest='MaxClient')
    args = parser.parse_args()

    return args


def config():
    '''综合当前配置'''
    args = _param()
    configFile = args.configFile
    if not os.path.exists(configFile):
        sys.exit('config file "'+configFile+'" not exists')
    config_dic = readconfig(configFile)
    print('Current config information:')
    table = prettytable.PrettyTable(('option', 'value'))
    table.align = 'l'
    for arg in args._get_kwargs():
        if arg[1]:
            config_dic[arg[0]] = arg[1]
        table.add_row((arg[0], config_dic[arg[0]]))
    if not os.path.exists(config_dic['CGIpath']):
        sys.exit('CGIpath "'+config_dic['CGIpath']+'"not found')
    if not os.path.exists(config_dic['wwwpath']):
        sys.exit('wwwpath "'+config_dic['wwwpath']+'"not found')
    if not os.path.exists(config_dic['default']):
        sys.exit('default "'+config_dic['default']+'"not found')
    if not (0 < config_dic['port'] < 65535):
        sys.exit('port '+str(config_dic['port'])+' out of range')

    print(table)
    print('Loading config')
    return config_dic


def readconfig(configFile):
    '''读取配置文件'''
    parser = configparser.ConfigParser()
    parser.read(configFile)
    CGIpath = parser.get('default', 'cgipath')
    wwwpath = parser.get('default', 'wwwpath')
    default = parser.get('default', 'default')
    TimeOut = parser.get('default', 'timeout')
    port = parser.get('default', 'port')
    MaxClient = parser.get('default', 'maxclient')
    dic = {'CGIpath': CGIpath, 'MaxClient': int(MaxClient), 'TimeOut': int(TimeOut),
           'configFile': configFile, 'default': default, 'port': int(port), 'wwwpath': wwwpath}
    return dic


def connect(sock, info, config_dic):
    print('proc ', os.getpid(), 'now handling connection from', info)
    while True:
        http = sock.recv(65535)
        if not http:
            break
        http = http.decode('utf8')
        request = parser(http, config_dic)
        packet = response(request, config_dic)
        sock.send(packet)
    print('client disconnect')


def parser(http: str, config_dic):
    request = Request()
    status_code = 0
    # 确定请求类型
    if 'GET' == http[0:3]:
        req_type = 'GET'
    elif 'POST' == http[0:4]:
        req_type = 'POST'
    # 分割head和body
    head = http.split('\r\n\r\n')[0]
    if len(http.split('\r\n\r\n')) == 2:
        body = http.split('\r\n\r\n')[1]
        request.body = body
        print('###http_body', body)
    # 分割head内segment
    head_op = head.split('\r\n')
    head_dic = {}
    for segment in head_op:
        desc = segment.split(' ')[0]
        if ':' in desc:
            desc = desc[:-1]
        param = []
        for item in segment.split(' ')[1:]:
            if ';' in item or ')' in item:
                item = item[:-1]
            if '(' in item:
                item = item[1:]
            param.append(item)
        param = tuple(param)
        head_dic[desc] = param
    print('###http_head:', head_dic)

    # 关键字段解析
    req_path = head_dic[req_type][0]
    http_version = head_dic[req_type][1]
    host = head_dic['Host'][0]
    browser = head_dic['User-Agent'][0]
    client_os = head_dic['User-Agent'][3]
    language = head_dic['Accept-Language']
    connection = head_dic['Connection']

    # 处理请求
    req_param = []
    if '?' in req_path:
        req_param.append(req_path.split('?')[1])
        req_path = req_path.split('?')[0]
    if req_param and '&' in req_param[0]:
        handle_list = req_param[0].split('&')
        req_param = []
        for param in handle_list:
            if '=' in param:
                req_param.append(param.split('=')[1])
            else:
                req_param.append(param)

    if '../' in req_path or './' in req_path:
        request.status = -1
        request.status_code = 400
        return request

    req_path = config_dic['wwwpath']+req_path
    print('###req_path', req_path)

    # 处理POST方法
    if req_type == 'POST':
        if body and '&' in body:
            handle_list = body.split('&')
        else:
            handle_list = (body)
        req_param = []
        for param in handle_list:
            if '=' in param:
                req_param.append(param.split('=')[1])
            else:
                req_param.append(param)
        req_type = 'GET'

    # 处理GET方法
    if req_type == 'GET':
        if os.path.isdir(req_path):
            if req_path == config_dic['wwwpath'] + '/':
                req_path = config_dic['default']
                request.status_code = 200
                request.status = 0
                request.is_html_file = 1
                request.path = req_path
                return request
            if req_path[-1] != '/':
                req_path += '/'
            request.is_dir = 1
            request.path = req_path
            request.status = 0
            request.status_code = 200
            return request
        elif os.path.isfile(req_path):
            # 文件是否是cgi或html或其他资源文件
            # 资源文件暂时只支持jpg
            if '.html' == req_path[-5:]:
                request.status_code = 200
                request.status = 0
                request.is_html_file = 1
                request.path = req_path
                return request
            elif '.py' == req_path[-3:] and config_dic['CGIpath'] in req_path:
                if req_param:
                    request.cgi_param = req_param
                request.status_code = 200
                request.status = 0
                request.is_cgi_file = 1
                request.path = req_path
                return request
            elif '.jpg' == req_path[-4:]:
                request.status_code = 200
                request.status = 0
                request.is_src_file = 1
                request.path = req_path
                request.http_type = 'image/jpeg'
                return request
            elif '.pdf' == req_path[-4:]:
                request.status_code = 200
                request.status = 0
                request.is_src_file = 1
                request.path = req_path
                request.http_type = 'application/pdf'
                return request
            elif '.png' == req_path[-4:]:
                request.status_code = 200
                request.status = 0
                request.is_src_file = 1
                request.path = req_path
                request.http_type = 'image/png'
                return request
            else:
                request.status_code = 404
                request.status = -1
                return request
        else:
            request.status_code = 404
            request.status = -1
            return request


def response(request, config_dic):
    print('###status', request.status)
    print('###code', request.status_code)
    if request.status == 0:
        if request.is_html_file:
            h_file = open(request.path)
            http_body = h_file.read()
            h_file.close()
        elif request.is_dir:
            http_body = '<html><head>current dir</head><body>'
            print('###path', request.path)
            dir_list = os.listdir(request.path)
            print('###dir_list', dir_list)
            for direc in dir_list:
                print('###', request.path+direc)
                if os.path.isdir(request.path+direc):
                    http_body += '<a href="' + \
                        request.path[len(config_dic['wwwpath'])
                                         :]+direc+'">'+direc+'</a>'
                if os.path.isfile(request.path+direc):
                    http_body += '<div>'+direc+'</div>'
            http_body += '</body></html>'
        elif request.is_cgi_file:
            execu = 'python3 '+request.path
            if request.cgi_param:
                for param in request.cgi_param:
                    execu += ' '+param
            cgi_pipe = os.popen(execu)
            http_body = cgi_pipe.read()
            cgi_pipe.close()
            print('###cgi return', http_body)
        elif request.is_src_file:
            srcfile = open(request.path,'rb')
            http_body = srcfile.read()
            http_body = http_body
            srcfile.close()
        else :
            pass
    elif request.status == -1:
        http_body = ''

    if not request.http_type:
        request.http_type = 'text/html'
    packet = pack(request.status_code,request.http_type,http_body)
    return packet


def pack(status_code,http_type, http_body):
    header = 'HTTP/1.1 '+str(status_code)+'\r\n' +\
        'Connection: keep-alive\r\n' +\
        'Content-Type: %s\r\n'%http_type +\
        'Status: %s\r\n'%str(status_code) +\
        'Content-Length: '+str(len(http_body))+'\r\n' +\
        '\r\n\r\n'
    if isinstance(http_body,bytes):
        packet = header.encode('utf8') + http_body
    else:
        packet = header+http_body
        packet = packet.encode('utf8')
    print(header)
    return packet


def main():
    wait_queue = []
    proc_pool = []
    conf_dic = config()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 8080))
    s.listen(65535)
    pid = os.getpid()
    print('main proc pid =', pid)
    check = threading.Thread(target=check_alive, args=(proc_pool,))
    check.setDaemon(True)
    check.start()
    while True:
        print('0x0:waiting for connection ......')
        con, info = s.accept()
        print('0x0:get new connection')
        wait_queue.append((con, info))
        if len(proc_pool) < conf_dic['MaxClient']:
            print('here')
            connection = wait_queue[-1]
            proc = multiprocessing.Process(target=connect, args=(
                connection[0], connection[1], conf_dic,))
            proc.daemon = True
            proc_pool.append(proc)
            proc.start()


def check_alive(pool):
    while True:
        del_pool = []
        for proc in pool:
            if not proc.is_alive():
                del_pool.append(proc)

        for proc in del_pool:
            pool.remove(proc)

        time.sleep(0.01)


if __name__ == '__main__':
    main()
