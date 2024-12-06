import scrapy
from datetime import datetime
from scrapy.spiders import SitemapSpider

#import json
#import os

"""
Method : 2
The https://blockworks.co/robots.txt has sitemap xml

To Crawl this website we need to 

1: go to https://blockworks.co/search
2: find sitemap.xml for news https://blockworks.co/news-sitemap-index.xml
3: visit every sub sitemap in sitemap xml
4: obey robots.txt, use roataing useragent in settings, limit pages downloaded to 20
5: enable deltafetch extension to prevent re-visiting articles already tracked
6: log every website before parsing for debugging 
7: we than parse for...
    {
    'source_name': websiter name 
    'source_type': news or social
    'date': year-month-day (we need to format this with a func)
    'cryptocurrency': array of every crypto mentioned in article (anything not in crypto list is not saved)
    'title': the title of the article
    'url': article url
    'text': all article text 
}

8: finally send the parsed data to the aggregator

"""

class BlockworkSpider(SitemapSpider):
   
    def __init__(self, *args, **kwargs ):
        super().__init__(*args, **kwargs)
        self.out_pipe = kwargs['out_pipe']

    name = 'BlockworkSpider'
    allowed_domains = ['blockworks.co']
    sitemap_urls = ['https://blockworks.co/news-sitemap-index.xml']
    sitemap_rules = [('/news/', 'parse_article')]

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
        
        #'CLOSESPIDER_ITEMCOUNT': 2, 

        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1.0,  
        'AUTOTHROTTLE_MAX_DELAY': 10.0, 
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,  
        'AUTOTHROTTLE_DEBUG': False,  

        'ROBOTSTXT_OBEY': True,
        'FEED_EXPORT_ENCODING': 'utf-8',
        
        'DELTAFETCH_ENABLED': True,
        'DELTAFETCH_DIR': 'visites',
    }

    def parse_article(self, response):
        
        url = response.url
        self.logger.info(f"Processing article: {url}")

        source_name = "Blockworks"
        source_type = "news"

        raw_date = response.xpath('/html/body/div[1]/div/main/section[1]/div[1]/article/div[1]/div[2]/div/div[2]/time/text()').get()
        formatted_date = self.format_date(raw_date) if raw_date else "Unknown"

        title = response.xpath('/html/body/div[1]/div/main/section[1]/div[1]/article/div[1]/h1/text()').get()

        text_xpath = '//*[@id="__next"]/div/main/section[1]/div[1]/article/div[3]/div[2]/section[1]/div//text()'
        paragraphs = response.xpath(text_xpath).getall()
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
                    'title': title if title else "Unknown",
                    'url': url,
                    'text': article_text,
                }
            ]
        }
        
    def format_date(self, raw_date):
        try:
            parsed_date = datetime.strptime(raw_date, "%B %d, %Y %I:%M %p")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            self.logger.warning(f"Failed to parse date: {raw_date}")
            return raw_date

    def extract_cryptocurrencies(self, text):
        mentioned_cryptos = []
        for key, value in self.CRYPTO_LIST.items():
            if key.lower() in text.lower():
                if value not in mentioned_cryptos:
                    mentioned_cryptos.append(value)
        return mentioned_cryptos


"""
Method : 1 
The https://blockworks.co/robots.txt does allow searchs 

To Crawl this website we need to 

1: go to https://blockworks.co/search
2: simulate the API endpoint https://eh58zikx8p-dsn.algolia.net/1/indexes/wp_posts_post/query (POST response)
3: find and use the correct api headers
4: use a user agent with refer https://blockworks.co/search
5: query every term from our crypto list 
6: while storing every articale that is returned 
7: we than parse for...
    {
    'source_name': websiter name 
    'source_type': news or social
    'date': year-month-day
    'cryptocurrency': array of every crypto mentioned in article
    'title': the title of the article
    'url': article url
    'text': all article text 
}

8: finally send the parsed data to the aggregator

"""

"""
class BlockworkSpider(scrapy.Spider):
    name = "BlockworkSpider"
    allowed_domains = ['blockworks.co', 'eh58zikx8p-dsn.algolia.net']
    start_urls = ['https://blockworks.co/search']

    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 1, 
    }

    def start_requests(self):
        url = "https://eh58zikx8p-dsn.algolia.net/1/indexes/wp_posts_post/query"
        headers = {
            "x-algolia-agent": "Algolia for JavaScript (4.24.0); Browser (lite)",
            "x-algolia-api-key": "b4d5d7a328a8d7d3896e04e0113b6282",
            "x-algolia-application-id": "EH58ZIKX8P",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Referer": "https://blockworks.co/search"
        }
        body = {
            "query": "Solana",  
            "hitsPerPage": 20,
            "page": 0
        }
        yield scrapy.Request(
            url=url,
            method="POST",
            headers=headers,
            body=json.dumps(body),
            callback=self.parse_api_response
        )

    def parse_api_response(self, response):
        data = response.json()
        hits = data.get("hits", [])
        if hits:
            # Work with only the first article
            first_article = hits[0]
            title = first_article.get("post_title", "Unknown")
            url = first_article.get("post_url", "Unknown")
            date = first_article.get("post_date", "Unknown")
            content = first_article.get("content", "No content available")
            formatted_date = self.format_date(date) if isinstance(date, str) else "Unknown"

            # Extract cryptocurrencies mentioned in the article text
            cryptocurrencies = self.extract_cryptocurrencies(content)

            yield {
                'source_name': 'blockworks',
                'source_type': 'news',
                'date': formatted_date,
                'cryptocurrency': cryptocurrencies if cryptocurrencies else [],
                'title': title,
                'url': url,
                'text': content,
            }
        else:
            self.logger.warning("No hits found in API response")

    def format_date(self, raw_date):
        try:
            # Assuming the raw date is in UNIX timestamp format
            parsed_date = datetime.fromtimestamp(int(raw_date))
            return parsed_date.strftime("%Y-%m-%d")  # Format to YYYY-MM-DD
        except (ValueError, TypeError):
            self.logger.warning(f"Failed to parse date: {raw_date}")
            return "Unknown"

    def extract_cryptocurrencies(self, text):
        crypto_mapping = {
            'Bitcoin': 'Bitcoin',
            'BTC': 'Bitcoin',
            'Ethereum': 'Ethereum',
            'ETH': 'Ethereum',
            'Solana': 'Solana',
            'SOL': 'Solana',
            'Ripple': 'Ripple',
            'XRP': 'Ripple',
            'Litecoin': 'Litecoin',
            'LTC': 'Litecoin'
        }
        mentioned_cryptos = []
        for key, value in crypto_mapping.items():
            if key.lower() in text.lower():
                if value not in mentioned_cryptos:
                    mentioned_cryptos.append(value)
        return mentioned_cryptos

'''      Handle pagination if applicable
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
'''
'''        article_links = response.css('a.article-card::attr(href)').getall()
        for link in article_links:
            yield response.follow(link, self.parse_article)
'''
            
            
"""

