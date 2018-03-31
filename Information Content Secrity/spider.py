# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import prettytable
import sys

def getCar():
    web = requests.get('http://top.baidu.com/buzz?b=1548&fr=topboards')
    web.encoding = web.apparent_encoding
    soup = BeautifulSoup(web.text,'html.parser')
    board = soup.body.findAll('a', 'list-title')
    print('百度热搜豪车榜:')
    table = prettytable.PrettyTable(('排名','车名'),encoding = 'utf-8')
    number = 0
    for tag in board:
        number += 1
        table.add_row((repr(number),str(tag.string)))
    print(table)
    
def getSch2016():
    web = requests.get('http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html')
    web.encoding = web.apparent_encoding
    soup = BeautifulSoup(web.text,'html.parser')
    form = soup.find('tbody','hidden_zhpm')
    pretty = prettytable.PrettyTable(('排名','学校名称','省市','总分','指标得分'))
    max =0
    for trow in form.contents:
        if trow.string == '\n':
            continue
        if max >= 30:
            break
        tableline = []
        count = 0
        for tag in trow.contents:
            if tag.string == '\n':
                continue
            if count == 5:
                break
            tableline.append(str(tag.string))
            count += 1
        pretty.add_row(tableline)
        max += 1
    print('2016最好大学排行')
    print(pretty)

def getSch2017():
    web = requests.get('http://www.zuihaodaxue.cn/zuihaodaxuepaiming2017.html')
    web.encoding = web.apparent_encoding
    soup = BeautifulSoup(web.text,'html.parser')
    form = soup.find('tbody','hidden_zhpm')
    # trow = form.tr.td.contents
    # print(trow[1].string)
    pretty = prettytable.PrettyTable(('排名','学校名称','省市','总分','指标得分'))
    max =0
    for trow in form.contents:
        if trow.string == '\n':
            continue
        if max >= 30:
            break
        tableline = []
        count = 0
        for tag in trow.td.contents:
            if tag.string == '\n':
                continue
            if count == 5:
                break
            tableline.append(str(tag.string))
            count += 1
        pretty.add_row(tableline)
        max += 1
    print('2017最好大学排行')
    print(pretty)

def getARWU2016():
    web = requests.get('http://www.zuihaodaxue.cn/ARWU2016.html')
    web.encoding = web.apparent_encoding
    soup = BeautifulSoup(web.text,'html.parser')
    form = soup.find('tbody')
    pretty = prettytable.PrettyTable(('排名','学校名称','国家排名','总分','指标得分'))
    max =0
    for trow in form.contents:
        if trow.string == '\n':
            continue
        if max >= 30:
            break
        tableline = []
        count = 0
        for tag in trow.contents:
            if tag.string == '\n':
                continue
            elif count == 6:
                break
            elif count == 1:
                tableline.append(str(tag.a.string))
            elif count == 2:
                pass
            else:
                tableline.append(str(tag.string))
            count += 1
        pretty.add_row(tableline)
        max += 1
    print('2016世界大学学术排名')
    print(pretty)

def getBook():
    web = requests.get('http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2014-0-1-1')
    web.encoding = web.apparent_encoding
    soup = BeautifulSoup(web.text,'html.parser')
    form = soup.find('ul','bang_list clearfix bang_list_mode')
    pretty = prettytable.PrettyTable(('排名','书名','作者','出版社','现价','原价')) # 
    # print( form.contents)
    for li in form.find_all('li'):
        row = []
        for div in li.find_all('div'):
            if div['class'][0] == 'list_num':
                row.append((str(div.string))[0:-1])
            elif div['class'][0] == 'name':
                row.append(str(div.a.string))
            elif div['class'][0] == 'publisher_info':
                string = ''
                for tag in div.contents:
                    string += str(tag.string)
                row.append(string)
            elif div['class'][0] == 'price':
                for span in div.find_all('span'):
                    row.append(str(span.string))
        while len(row) != 6:
            row.remove(row[-1])
        pretty.add_row(row)
    print('当当图书2014年图书畅销榜')
    print(pretty)
        
if __name__ == '__main__':
    getBook()