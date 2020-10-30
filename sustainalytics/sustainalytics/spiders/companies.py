import scrapy

from selenium.webdriver.common.keys import Keys

from scrapy_selenium import SeleniumRequest


class CompaniesSpider(scrapy.Spider):
    name = 'companies'

    # def __init__(self):
    #     options = webdriver.ChromeOptions()
    #     options.add_argument("--headless")
    #     options.binary_location = '/opt/brave.com/brave/brave-browser'

    #     driver = webdriver.Chrome(
    #         executable_path='/home/ns/ScrapyProjects/sustainalytics/chromedriver', options=options)
    #     driver.get("https://www.sustainalytics.com/esg-ratings/")

    #     self.html = driver.page_source
    #     driver.close()

    def start_requests(self):
        yield SeleniumRequest(url="https://www.sustainalytics.com/esg-ratings/",
                              wait_time=2,
                              screenshot=True,
                              callback=self.parse
                              )

    def parse(self, response):
        # driver = response.meta['driver']
        # driver.save_screenshot('show.png')

        for page in range(1, 3):
            print(page)
            yield SeleniumRequest(url=f"https://www.sustainalytics.com/esg-ratings/?currentpage={page}",
                                  wait_time=2,
                                  callback=self.parse_page)

    def parse_page(self, response):
        companies = response.xpath(
            '//div[@class="company-row d-flex"]//a/@href').extract()

        for company in companies:
            yield SeleniumRequest(url=response.urljoin(company),
                                  wait_time=1,
                                  callback=self.parse_company)

    def parse_company(self, response):
        yield {
            'identifier': response.xpath('//strong[@class="identifier"]/text()').get(),
            'name': response.xpath('//h2[@class=""]/text()').get(),
            'country': response.xpath('//strong[@class="country"]/text()').get(),
            'industry': response.xpath('(//strong[@class="industry-group"]/text())[1]').get(),
            'esg_score': response.xpath('(//span[@class=""]/text())[1]').get(),
            'industry_rank': response.xpath('//strong[@class="industry-group-position"]/text()').get(),
            'global_rank': response.xpath('//strong[@class="universe-position"]/text()').get(),
        }
