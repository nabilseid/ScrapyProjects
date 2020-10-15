import scrapy


class BestsellersSpider(scrapy.Spider):
    name = 'bestsellers'
    allowed_domains = ['www.glassesshop.com/bestsellers']
    start_urls = ['http://www.glassesshop.com/bestsellers/']

    def parse(self, response):
        pass
