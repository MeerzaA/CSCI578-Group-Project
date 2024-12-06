import scrapy
from datetime import datetime
from scrapy.spiders import SitemapSpider

"""
Method : 2
The https://decrypt.co/robots.txt allows sitemap xml

To Crawl this website we need to 

1: go to https://decrypt.co/robots.txt
2: find sitemap.xml for news https://decrypt.co/news-sitemap-index.xml
3: visit every sub sitemap in sitemap xml
4: obey robots.txt, use roataing useragent in settings, limit pages downloaded to 20
5: enable deltafetch extension to prevent re-visiting articles already tracked
6: log every website before parsing for debugging 
7: search for bread crumbs that match a news page 
8: we than parse for...
    {
    'source_name': websiter name 
    'source_type': news or social
    'date': year-month-day (we need to format this with a func)
    'cryptocurrency': array of every crypto mentioned in article (anything not in crypto list is not saved)
    'title': the title of the article
    'url': article url
    'text': all article text 
}

9: finally send the parsed data to the aggregator

"""

class DecryptSpider(SitemapSpider):
    
    def __init__(self, *args, **kwargs ):
        super().__init__(*args, **kwargs)
        self.out_pipe = kwargs['out_pipe']
    
    name = "DecryptSpider"
    allowed_domains = ["decrypt.co"]
    sitemap_urls = ["https://decrypt.co/sitemap_index.xml"] 
    sitemap_rules = [(r'/\d+/', 'parse_article')] # regex a random number is always the first extension after the allowed domain for some reason on this site 
    
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
        'Binance Coin': 'Binance Coin',
        'BNB' : 'Binance Coin',
        'Cardano': 'Cardano',
        'ADA': 'Cardano',
        'Avalanche': 'Avalanche',
        'AVAX': 'Avalanche',
        'Shiba Inu': 'Shiba Inu',
        'SHIB': 'Shiba Inu',
    }

    
    custom_settings = {
        
        #'CLOSESPIDER_ITEMCOUNT': 2,
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
    
    def parse_article(self, response):
        url = response.url
        self.logger.info(f"Processing article: {url}")

        # Breadcrumb extraction
        breadcrumb_xpath = (
            '//div[contains(@class, "flex flex-wrap items-center whitespace-nowrap")]/a/span/text()'
        )
        breadcrumbs = response.xpath(breadcrumb_xpath).getall()
        self.logger.info(f"Breadcrumbs extracted: {breadcrumbs}")

        if "News" in breadcrumbs:
            self.logger.info(f"Matched breadcrumbs: {breadcrumbs} at {response.url}")
        else:
            self.logger.info(f"No matching breadcrumbs found for {url}")
            return

        # Extract source details
        source_name = "Decrypt"
        source_type = "news"

        # Extract and format the date
        raw_date = response.xpath(
            '//span[contains(@class, "font-akzidenz-grotesk")]/time[1]/@datetime'
        ).get()
        self.logger.info(f"Raw date extracted: {raw_date}")
        formatted_date = self.format_date_from_datetime(raw_date) if raw_date else "Unknown"

        # Extract title
        title = response.xpath('//h1/text()').get()

        # Extract article text
        text_xpath = '//div[contains(@class, "post-content")]//p/text()'
        paragraphs = response.xpath(text_xpath).getall()
        article_text = " ".join([p.strip() for p in paragraphs])


                    
        # Extract mentioned cryptocurrencies
        cryptocurrencies = self.extract_cryptocurrencies(article_text)
        self.logger.info(f"Cryptocurrencies extracted: {cryptocurrencies}")

        # Skip articles with no mentioned cryptocurrencies
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


    def format_date_from_datetime(self, raw_date):
        try:
            # Use the datetime value directly
            parsed_date = datetime.strptime(raw_date[:10], "%Y-%m-%d")
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
Method : 1 This kept crashing 
The https://decrypt.co/robots.txt has no restrictions whats so ever

To Crawl this website we need to 

1: go to https://decrypt.co/search
2: This website dynamiclly loads its search results, with graphql 
3: We need to track down the api endpoint, and than simulate a post request as this is the only way to query 
    check: https://gateway.decrypt.co/?variables=%7B%22filters%22%3A%7B%22locale%22%3A%7B%22eq%22%3A%22en%22%7D%2C%22or%22%3A%5B%7B%22title%22%3A%7B%22contains%22%3A%22bitcoin%22%7D%7D%2C%7B%22excerpt%22%3A%7B%22contains%22%3A%22bitcoin%22%7D%7D%2C%7B%22content%22%3A%7B%22contains%22%3A%22bitcoin%22%7D%7D%5D%7D%2C%22pagination%22%3A%7B%22pageSize%22%3A10%7D%2C%22sort%22%3A%5B%22_score%3Adesc%22%5D%7D&operationName=ArticlePreviews&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227366f3114618c1df3a4b718a7b3e6f93cb804c036a907f52a75b108d9645618f%22%7D%7D
4: Run a seach on the browser, and copy and paste the user agent from the header tab, [no idea why this is the only thing that works]
5: query every term from our crypto list 
6: 
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

