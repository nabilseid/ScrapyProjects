import scrapy


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net']
    start_urls = ['http://www.livecoin.net/']

    def parse(self, response):
        pass
