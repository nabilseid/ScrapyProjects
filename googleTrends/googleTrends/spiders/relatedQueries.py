import scrapy

from scrapy.selector import Selector

from selenium.webdriver.common.keys import Keys

from scrapy_selenium import SeleniumRequest

from time import sleep


class RelatedqueriesSpider(scrapy.Spider):
    name = 'relatedQueries'

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    # //explore?q=zoom%20background&geo=US

    def start_requests(self):
        yield SeleniumRequest(url="https://trends.google.com/trends/",
                              wait_time=5,
                              #   screenshot=True,
                              callback=self.parse,
                              headers={'User-Agent': self.user_agent}
                              #            'cookie': '__utma=10102256.148149822.1604100468.1604100468.1604100468.1; __utmc=10102256; __utmz=10102256.1604100468.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=10102256.2.10.1604100468; ANID=AHWqTUlaph93Wf--I9uG_tG8RqxjTnbba6U6p25yo110dTZpr6c3-79DbrItrfCn; 1P_JAR=2020-10-30-23; NID=204=p-wQcqK77nnKGjX6ulY7TDEo4FvG7fEsryS8qIWbsCC2UXL9HBG-VmNk_honG-KtYwxYhsrI7VG-OKD9XTY5r1a7JCRLyyKSyxgB0-P92o0zPXgTAO9O9nUdJixWVT-ebv0dvy9-HcbS1Kj3OnC6Jl6LxnvAAvq-021oeiqWa78'}
                              )

    def parse(self, response):

        driver = response.meta['driver']

        search_input = driver.find_element_by_xpath(
            '(//autocomplete)[2]//input')
        search_input.send_keys('zoom backgrounds')

        search_input.send_keys(Keys.ENTER)

        sleep(1)

        res_obj = Selector(text=driver.page_source)

        queries = res_obj.xpath(
            '(//div[@class="content-wrap"])[2]/div/div[4]//span/text()').getall()

        print(queries[:5])
