import re
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import requests
import threading

url_list = None

def get_苹果():
    url = 'https://s.taobao.com/search?q=苹果'
    http = requests.get(url)
    http.encoding = http.apparent_encoding
    plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
    tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
    ilt = PrettyTable(('序号','价格','名称'))
    for i in range(len(plt)):
        price = eval(plt[i].split(':')[1])
        title = eval(tlt[i].split(':')[1])
        ilt.add_row([i,price, title])
    ilt.align = 'l'
    print(ilt)

def get_stocklist():
    url = 'http://quote.eastmoney.com/stocklist.html'
    http = requests.get(url)
    http.encoding = http.apparent_encoding
    html = http.text
    soup = BeautifulSoup(html,'html.parser')
    url_list = soup.find_all('a',href=re.compile('^http://quote\.eastmoney\.com/s[zh]\d+\.html'))
    file = open('url_list','w')
    for url in url_list:
        file.writelines('https://gupiao.baidu.com/stock/' + re.search('s[zh]\d+',str(url['href'])).group() + '.html'+'\n')
    file.close()

def get_stock(controller):
    while True:
        try:
            url = controller.get_url()
            if url == False:
                break
            http = requests.get(url)
            http.encoding = http.apparent_encoding
            html = http.text
            # if re.search('class="price s-stop "',html):
            #     if not re.search('class="line1"',html):
            #         soup = BeautifulSoup(html,'html.parser')
            #         info = soup.find('a','bets-name')
            #         tmp = []
            #         for string in info.stripped_strings:
            #             tmp.append(string)
            #         name = tmp[0][0:-2]
            #         number = tmp[1][0:]
            #         bet = {'股票名称':name,'股票代码':number}
            #         controller.add_bets(bet)
            soup = BeautifulSoup(html,'html.parser')
            info = soup.find('a','bets-name')
            tmp = []
            for string in info.stripped_strings:
                tmp.append(string)
            name = tmp[0][0:-2]
            number = tmp[1][0:]
            bet = {'股票名称':name,'股票代码':number}

            price = soup.find('div',('price'))
            if price != None:
                bet['现价'] = repr(price.strong.string)

            details = soup.find('div','bets-content')
            if details !=None:
                div = details.find('div','line1')
                if div != None:
                    for dl in div.find_all('dl'):
                        bet[repr(dl.dt.string)] = repr(dl.dd.string)
                div = details.find('div','line2')
                if div != None
                    for dl in div.find_all('dl'):
                        bet[repr(dl.dt.string)] = repr(dl.dd.string)

            controller.add_bets(bet)
        except Exception as e:
            print(repr(e),'\n',url)
            continue

class URL_controller():
    def __init__(self):
        urls = []
        self.bets_info = []
        file = open('./url_list','r')
        for line in file.readlines():
            urls.append(line[:-1])
        file.close()
        self.file = open('bets_info','w')

        self.urls = urls
        self.length = len(urls)
        self.next = 0
        self.lock = threading.Lock()
        self.strat_threading()
        for item in self.bets_info:
            self.file.writelines(repr(item)+'\n')
        self.file.close()

    def get_url(self):
        self.lock.acquire()
        if self.next >= self.length:
            return False
        url = self.urls[self.next]
        self.next += 1
        self.lock.release()
        return url
    
    def add_bets(self,bet):
        self.lock.acquire()
        self.bets_info.append(bet)
        self.lock.release()

    def strat_threading(self):
        for _ in range(100):
            thread = threading.Thread(target=get_stock,args=(self,))
            thread.start()
            thread.join()
    
if __name__ == '__main__':
    URL_controller()