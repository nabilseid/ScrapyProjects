import scrapy


class SingleBathroomVanitySpider(scrapy.Spider):
    name = 'single_bathroom_vanity'
    allowed_domains = ['www.homedepot.com']
    start_urls = ['https://www.homedepot.com/p/Boyel-Living-Denver-Collection-30-in-Single-Bathroom-Vanity-JMJ-BCB-1530-WH/314296512?MERCH=REC-_-rv_gm_pip_rr-_-314296576-_-314296512-_-N/']

    def parse(self, response):
        specs = response.xpath(
            '//div[@id="root"]//div[@name="specifications"]/div/div/div/div')[2:5]

        keys = []
        values = []

        for spec in specs:
            keys += spec.xpath('./div/div/div/div[1]/text()').extract()
            values += spec.xpath('./div/div/div/div[2]/text()').extract()
        
        yield dict(zip(keys, values))
