import scrapy
from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net/en']

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = False
            
            assert(splash:go(args.url))
            assert(splash:wait(1))
            
            tab_btn = assert(splash:select_all(".filterPanelItem___2z5Gb"))
            tab_btn[4]:mouse_click()
            assert(splash:wait(1))
            
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.livecoin.net/en",
                            callback=self.parse,
                            endpoint="execute",
                            args={'lua_source': self.script})

    def parse(self, response):
        print(len(response.xpath('//div[@class="ReactVirtualized__Grid__innerScrollContainer"]/div')))
