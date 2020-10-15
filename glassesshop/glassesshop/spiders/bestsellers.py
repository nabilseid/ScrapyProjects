import scrapy


class BestsellersSpider(scrapy.Spider):
    name = 'bestsellers'
    # allowed_domains = ['www.glassesshop.com/bestsellers']
    # start_urls = ['https://www.glassesshop.com/bestsellers']

    def start_requests(self):
        yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback=self.parse)

    def parse(self, response):
        products = response.xpath('//div[@id="product-lists"]/div')

        for product in products:
            product_content = product.xpath('.//div')

            if len(product_content) < 2:
                continue

            yield {
                'url': product_content[0].xpath('.//a/@href').get(),
                'img_url': product_content[0].xpath('.//a/img[1]/@src').get(),
                'name': product_content[1].xpath('.//div[@class="p-title"]/a/text()').get().strip(),
                'price': product_content[1].xpath('.//div[@class="p-price"]/div/span/text()').get().strip(),
            }

        next_page = response.xpath(
            '//li[@class="page-item"]/a[@rel="next"]/@href').get()
        print(next_page)
        if(next_page):
            yield scrapy.Request(url=next_page, callback=self.parse)