import re
import scrapy


class FeaturedProductsSpider(scrapy.Spider):
    name = 'featured_products'
    allowed_domains = ['www.cigabuy.com/featured_products.html']
    start_urls = ['https://www.cigabuy.com/featured_products.html']

    def parse(self, response):

        products = response.xpath('//div[@class="p_box_wrapper"]')

        for product in products:
            title = product.xpath('.//a[@class="p_box_title"]/text()').get()
            url = response.urljoin(product.xpath(
                './/a[@class="p_box_title"]/@href').get())
            rating = product.xpath('.//span/@class').get()
            price = product.xpath('.//div[@class="p_box_price cf"]')

            if(price.xpath('.//*')):
                discount_price = price.xpath('.//*[1]/text()').get()
                original_price = price.xpath('.//*[2]/text()').get()
            else:
                discount_price = None
                original_price = price.xpath('.//text()').get()

            yield {'title': title,
                   'url': url,
                   'rating': self.parse_rating(rating),
                   'discount_price': self.parse_price(discount_price),
                   'original_price': self.parse_price(original_price), }
        
        next_page = response.xpath('(//a[@class="nextPage"])[1]/@href').get()
        
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_price(self, price):
        if(price == None):
            return None

        print(price)
        return re.sub('[!$]', '', price)

    def parse_rating(self, rating):
        print(rating)
        if(rating == None):
            return None

        rating = rating.strip()
        rate = rating[-3:].split('_')
        try:
            leading_rate = int(rate[0])
        except:
            return int(rate[1])

        return leading_rate + (int(rate[1])/10)
