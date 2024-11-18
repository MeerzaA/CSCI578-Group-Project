import scrapy

class BinsiderspriderSpider(scrapy.Spider):
    name = "BInsiderSpider"
    allowed_domains = ["businessinsider.com"]
    start_urls = ["https://www.businessinsider.com/"]

    def parse(self, response):
        # Extract article titles and links
        Tout_Titles = response.css('h3.tout-title')
        
        for title in Tout_Titles:
            name = title.css('a.tout-title-link::text').get()
            relative_url = title.css('a.tout-title-link::attr(href)').get()
            
            if name and relative_url:  # Ensure both title and URL exist
                full_url = response.urljoin(relative_url)
                yield {
                    'name': name.strip(),
                    'url': full_url,
                }
                # Follow the article link
                yield response.follow(full_url, self.parse_details)

    def parse_details(self, response):
   
        content = ' '.join(response.css('div.article-content p::text').getall())
        yield {
            'url': response.url,
            'content': content.strip() if content else 'No content available',
        }

