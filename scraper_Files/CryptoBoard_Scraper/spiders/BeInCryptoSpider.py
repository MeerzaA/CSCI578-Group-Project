import scrapy
from datetime import datetime, timedelta
from scrapy.spiders import SitemapSpider

#import json
#import os

"""
Method : 1
The https://BeInCrryptoSpider.com/robots.txt allows sitemap xml

To Crawl this website we need to 

1: go to https://BeInCrryptoSpider.com/news/
2: find the element with all article links
3: visit every article on page and log every website before parsing for debugging  
4: we than parse for...
    {
    'source_name': websiter name 
    'source_type': news or social
    'date': year-month-day (we need to format this with a func)
    'cryptocurrency': array of every crypto mentioned in article (anything not in crypto list is not saved)
    'title': the title of the article
    'url': article url
    'text': all article text 
}
5: do this for all articles until we get to the last page which we can find out at the bottom
6: enable deltafetch extension to prevent re-visiting articles already tracked
7: finally send the parsed data to the aggregator

"""

class BeInCrryptoSpider(scrapy.Spider):
    
    def __init__(self, *args, **kwargs ):
        super().__init__(*args, **kwargs)
        self.out_pipe = kwargs['out_pipe']
    
    name = 'BeInCryptoSpider'
    allowed_domains = ['beincrypto.com']
    start_urls = ['https://beincrypto.com/news/']

    CRYPTO_LIST = {
        'Bitcoin': 'Bitcoin',
        'BTC': 'Bitcoin',
        'Ethereum': 'Ethereum',
        'ETH': 'Ethereum',
        'Solana': 'Solana',
        'SOL': 'Solana',
        'Ripple': 'Ripple',
        'XRP': 'Ripple',
        'Litecoin': 'Litecoin',
        'LTC': 'Litecoin',
        'Dogecoin': 'Dogecoin',
        'DOGE': 'Dogecoin',
        'BNB': 'BNB',
        'Cardano': 'ADA',
        'ADA': 'Cardano',
        'Avalanche': 'AVAX',
        'AVAX': 'Avalanche',
        'Shiba Inu': 'SHIB',
        'SHIB': 'Shiba Inu',
    }

    custom_settings = {
        
        #'CLOSESPIDER_ITEMCOUNT': 2, # limit for testing only
        'CONCURRENT_REQUESTS': 8, 

        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_MAX_DELAY': 10.0, 
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 5.0,  
        'AUTOTHROTTLE_DEBUG': False,  

        'ROBOTSTXT_OBEY': True,
        'FEED_EXPORT_ENCODING': 'utf-8',
        
        'DELTAFETCH_ENABLED': True,
        'DELTAFETCH_DIR': 'visites',
    }

    def parse(self, response):
  
        articles = response.css('div[data-el="bic-c-news-big"]')
        for article in articles:
            link = article.css('a::attr(href)').get()
            date_str = article.css('time.ago::text').get()
            if link and date_str:
                formatted_date = self.format_date(date_str)
                request = scrapy.Request(link, callback=self.parse_article)
                request.meta['publication_date'] = formatted_date
                yield request

        current_page = response.url.rstrip('/').split('/')[-1]
        if not current_page.isdigit():
            current_page = "1"
        next_page = int(current_page) + 1

        next_page_url = f'https://beincrypto.com/news/page/{next_page}/'
        yield response.follow(next_page_url, callback=self.parse)

    def parse_article(self, response):
        url = response.url
        self.logger.info(f"Processing article: {url}")

        source_name = "BeInCrypto"
        source_type = "news"

        formatted_date = response.meta.get('publication_date', 'Unknown')

        title = response.xpath('//article//header//h1/text()').get()
        title = title.strip() if title else "Unknown"

        paragraphs = response.xpath('//article//p//text()').getall()
        article_text = ' '.join([p.strip() for p in paragraphs if p.strip()])

        cryptocurrencies = self.extract_cryptocurrencies(article_text)

        if not cryptocurrencies:
            self.logger.info(f"Skipping article with no cryptocurrencies: {url}")
            return

        yield {
            "Scraped_Format": [
                {
                    'source_name': source_name,
                    'source_type': source_type,
                    'date': formatted_date,
                    'cryptocurrency': cryptocurrencies,
                    'title': title,
                    'url': url,
                    'text': article_text,
                }
            ]
        }

    def format_date(self, raw_date):
        try:
            date = datetime.strptime(raw_date.strip(), "%b %d, %Y")
        except ValueError:
            self.logger.warning(f"Unable to parse date: {raw_date}. Using current date instead.")
            date = datetime.now()
        return date.strftime("%Y-%m-%d")

    def extract_cryptocurrencies(self, text):
        mentioned_cryptos = []
        for key, value in self.CRYPTO_LIST.items():
            if key.lower() in text.lower():
                if value not in mentioned_cryptos:
                    mentioned_cryptos.append(value)
        return mentioned_cryptos