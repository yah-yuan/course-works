import scrapy

class TaobaoSpider(scrapy.Spider):
    name = 'Taobao'
    allowed_domains = ['taobao.com']
    start_urls = ['https://s.taobao.com/search?q=特斯拉']

