import scrapy


class BinsiderspriderSpider(scrapy.Spider):
    name = "BInsiderSprider"
    allowed_domains = ["www.businessinsider.com"]
    start_urls = ["https://www.businessinsider.com/"]

    def parse(self, response):
        pass
