from gensim.models import word2vec
from bs4 import BeautifulSoup
import re
import requests
import jieba
import logging

def Geturl(target,wikiurls):
    headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive', }
    page0 = requests.get(target,headers=headers)
    page0.encoding = page0.apparent_encoding
    html = page0.text
    soup = BeautifulSoup(html,'html.parser')
    link = soup.find_all('a')
    for a in link:
        try:
            url = str(a['href'])
        except Exception:
            continue
        if re.match('http://baike.baidu.com/view/',url):
            'http://baike.baidu.com/view/'
            if url not in wikiurls:
                wikiurls.append(url)

def Gettext(wikiurls):
    headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive', }
    count = 0
    file = open('baiduwiki','w+')
    for url in wikiurls:
        count += 1
        print('正在爬取第',str(count),'个页面',end = '\r')
        page0 = requests.get(url,headers=headers)
        page0.encoding = page0.apparent_encoding
        html = page0.text
        soup = BeautifulSoup(html,'html.parser')
        content = soup.find('div','main-content')
        text = str(content.text)
        text = text.strip()
        text = text.replace(' ','')
        text = text.replace('\n','')
        file.write(text)
    file.close()

def Getfenci():
    path = 'baiduwiki'
    file = open(path,'r')
    content = ''
    for newline in file.readlines():
        content += newline
    file.close()
    fenci = jieba.cut(content)
    file = open('fenci','w')
    for item in fenci:
        file.write(item+' ')
    #分词结束

def Getvec():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus('fenci') # 加载语料
    model = word2vec.Word2Vec(sentences, size=200) # 训练模型,维度设置为200;
    #test
    print('"刘备"的分词向量是:')
    print(model['刘备'])
    print('与"刘备"最相关的词是:')
    for item in model.most_similar("刘备", topn=20):
        print(item)


if __name__ == '__main__':
    # # 爬取要爬取的页面url
    # wikiurls = []
    # Geturl('http://baike.baidu.com/renwu',wikiurls)
    # Geturl('http://baike.baidu.com/jingji',wikiurls)
    # Geturl('http://baike.baidu.com/wenhua',wikiurls)
    # print('要爬取的页面总数为: ',len(wikiurls))
    # file = open('url_list','w+')
    # for item in wikiurls:
    #     file.writelines(item+'\n')
    # file.close()
    # # 爬取页面文字内容
    # Gettext(wikiurls)
    Getvec()