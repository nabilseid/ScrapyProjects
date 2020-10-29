from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which

import time
import json
from scrapy.selector import Selector


def scroll_down():
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.binary_location = '/opt/brave.com/brave/brave-browser'

driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
driver.get("https://cloud.withgoogle.com/partners?search=africa")

# https://cloud.withgoogle.com/partners/?regions=EMEA_REGION&products=GOOGLE_WORKSPACE_PRODUCT&sort-type=RELEVANCE

time.sleep(5)
scroll_down()

nxt_btn = driver.find_element_by_xpath(
    "//button[@id='load-more-cards-button']")

a = 1
while nxt_btn:
    print(a)
    nxt_btn.click()
    time.sleep(2)
    scroll_down()
    try:
        nxt_btn = driver.find_element_by_xpath(
            "//button[@id='load-more-cards-button']")
    except:
        break
    a += 1

html = driver.page_source

resp = Selector(text=html)
partners = resp.xpath('//div[@class="card"]/a/@href').getall()
print(len(partners))

final = []

for i, partner in enumerate(partners):
    print(i)
    driver.get('https://cloud.withgoogle.com' + partner)
    time.sleep(5)
    p_html = driver.page_source
    p_resp = Selector(text=p_html)
    title = p_resp.xpath('//div[@class="detail-hero__text"]/div[1]/text()').get()
    website = p_resp.xpath(
        '(//div[@class="detail-links__row"])[1]/a[@class="detail-links__link"][1]/@href').get()
    email = p_resp.xpath(
        '(//div[@class="detail-links__row"])[1]/a[@class="detail-links__link"][2]/@href').get()
    phone = p_resp.xpath(
        '(//div[@class="detail-links__row"])[1]/a[@class="detail-links__link"][3]/@href').get()

    final.append({'title': title, 'website': website,
                  'email': email, 'phone': phone})

json.dumps(final)
