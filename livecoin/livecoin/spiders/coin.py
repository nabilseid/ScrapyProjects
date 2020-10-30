import time
import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class CoinSpiderSelenium(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ['https://www.livecoin.net/en']

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.binary_location = '/opt/brave.com/brave/brave-browser'

        self.driver = webdriver.Chrome(
            executable_path='/home/ns/chromedriver', options=options)
        # self.driver.set_window_size(1920, 1080)
        self.driver.get(
            "https://cloud.withgoogle.com/partners/?regions=EMEA_REGION&products=GOOGLE_WORKSPACE_PRODUCT&sort-type=RELEVANCE")
        time.sleep(5)
        self.scroll_down()

        nxt_btn = self.driver.find_element_by_xpath(
            "//button[@id='load-more-cards-button']")
        
        a = 1
        while nxt_btn:
            print(a)
            nxt_btn.click()
            time.sleep(2)
            self.scroll_down()
            nxt_btn = self.driver.find_element_by_xpath(
            "//button[@id='load-more-cards-button']")
            a += 1

        self.html = self.driver.page_source
        self.driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        print(len(resp.xpath(
            '//div[@class="ReactVirtualized__Grid__innerScrollContainer"]/div')))

    def scroll_down(self):
        """A method for scrolling the page."""
        # Get scroll height.
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            # time.sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")

            if new_height == last_height:

                break

            last_height = new_height
