import scrapy
from datetime import datetime
import json


"""
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

class DecryptSpider(scrapy.Spider):
    
    name = "DecryptSpider"
    allowed_domains = ["decrypt.co"]
    start_urls = ["https://decrypt.co/news"]  # Adjust to the section or page you want to scrape

    def parse(self, response):
        # Extract articles
        for article in response.css('div.card'):  # Adjust the selector based on inspection
            title = article.css('h2::text').get()
            excerpt = article.css('p.excerpt::text').get()  # Adjust based on the site's structure
            url = article.css('a::attr(href)').get()
            publish_date = article.css('time::attr(datetime)').get()

            if url:
                url = response.urljoin(url)  # Ensure the URL is absolute

            yield {
                "title": title,
                "excerpt": excerpt,
                "url": url,
                "publish_date": publish_date,
            }

        # Pagination
        next_page = response.css('a.next-page::attr(href)').get()  # Adjust selector
        if next_page:
            yield response.follow(next_page, self.parse)
