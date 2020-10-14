import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info/']
    start_urls = [
        'https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath('//td/a')

        for country in countries:
            name = country.xpath('./text()').getall()
            link = country.xpath('./@href').getall()

            yield response.follow(url=link, callable=self.parse_country)

    def parse_country(self, response):
        rows = response.xpath(
            '(//div[@class="content-inner"]//table[contains(@class,"table table-striped")])[1]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/text()').get()

            yield {'year': year, 'population': population}
