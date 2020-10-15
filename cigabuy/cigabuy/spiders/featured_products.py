import scrapy


class FeaturedProductsSpider(scrapy.Spider):
    name = 'featured_products'
    allowed_domains = ['www.cigabuy.com/featured_products.html']
    start_urls = ['http://www.cigabuy.com/featured_products.html/']

    def parse(self, response):
        pass
